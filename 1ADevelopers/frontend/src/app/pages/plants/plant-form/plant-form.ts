import { Component, OnInit, inject } from '@angular/core';
import {
  ReactiveFormsModule,
  FormBuilder,
  FormGroup,
  FormArray,
  Validators,
  AbstractControl,
  ValidationErrors,
} from '@angular/forms';
import { PlantasServicio } from '../../../services/plantas-servicio';
import { Categoria } from '../../../interfaces/categoria';
import { Especie } from '../../../interfaces/especie';
import { RouterModule, Router, ActivatedRoute } from '@angular/router';

const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp'];

function imageUrlValidator(control: AbstractControl): ValidationErrors | null {
  const url: string = control.value?.trim() ?? '';
  if (!url) return null;

  try {
    new URL(url);
  } catch {
    return { invalidUrl: true };
  }

  const pathname = new URL(url).pathname.toLowerCase();
  const ext = pathname.split('.').pop() ?? '';
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    return { invalidExtension: { allowed: ALLOWED_EXTENSIONS.join(', '), actual: ext } };
  }
  return null;
}

@Component({
  selector: 'app-plant-form',
  imports: [ReactiveFormsModule, RouterModule],
  templateUrl: './plant-form.html',
  styleUrl: './plant-form.css',
})
export class PlantForm implements OnInit {
  private route = inject(ActivatedRoute);
  private fb = inject(FormBuilder);
  private PlantasServicio = inject(PlantasServicio);
  private router = inject(Router);

  form!: FormGroup;
  categorias: Categoria[] = [];
  submitStatus: 'idle' | 'loading' | 'success' | 'error' = 'idle';
  errorMessage = '';
  isEditMode: boolean = false;

  readonly maxImages = 6;

  ngOnInit(): void {
    this.buildForm();
    this.loadCategorias();

    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEditMode = true;

      this.PlantasServicio.getPlantaId(+id, true).subscribe({
        next: (data) => {
          this.form.patchValue({
            nombre_comun: data.nombre_comun,
            nombre_cientifico: data.nombre_cientifico,
            descripcion: data.descripcion,
            categoria: data.categoria,
          });
          this.imagenes.clear();
          data.imagenes.forEach((img: any) => {
            this.imagenes.push(
              this.fb.group({
                id: [img.id],
                url: [img.url, [Validators.required, imageUrlValidator]],
              }),
            );
          });
        },
        error: (err: any) => {
          console.error('Error al cargar la planta:', err);

          this.form.reset();

          if (err.status === 403 || err.status === 401) {
            alert(
              'Acceso denegado: No tienes permisos para consultar o editar esta ficha de planta.',
            );
          } else {
            alert('No se pudo encontrar la planta solicitada.');
          }
          this.router.navigate(['/docentes']);
        },
      });
    }
  }

  private buildForm(): void {
    this.form = this.fb.group({
      nombre_comun: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(100)]],
      nombre_cientifico: [
        '',
        [Validators.required, Validators.minLength(3), Validators.maxLength(150)],
      ],
      descripcion: [
        '',
        [Validators.required, Validators.minLength(10), Validators.maxLength(2000)],
      ],
      categoria: [null, Validators.required],
      imagenes: this.fb.array([this.createImagenControl()]),
    });
  }

  private createImagenControl(): FormGroup {
    return this.fb.group({
      url: ['', [Validators.required, imageUrlValidator]],
    });
  }

  get imagenes(): FormArray {
    return this.form.get('imagenes') as FormArray;
  }

  addImagen(): void {
    if (this.imagenes.length < this.maxImages) {
      this.imagenes.push(this.createImagenControl());
    }
  }

  removeImagen(i: number): void {
    if (this.imagenes.length > 1) {
      this.imagenes.removeAt(i);
    }
  }

  private loadCategorias(): void {
    this.PlantasServicio.getCategorias().subscribe({
      next: (data: Categoria[]) => (this.categorias = data),
      error: () => console.warn('Error al cargar categorías'),
    });
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.submitStatus = 'loading';
    const raw: Especie = this.form.getRawValue();
    const userSession = localStorage.getItem('user');
    let usuarioId = 1;

    if (userSession) {
      const user = JSON.parse(userSession);
      usuarioId = user.id;
    }

    const payload: Especie = {
      nombre_comun: raw.nombre_comun.trim(),
      nombre_cientifico: raw.nombre_cientifico.trim(),
      descripcion: raw.descripcion.trim(),
      categoria: Number(raw.categoria),
      usuario: usuarioId,
      imagenes: raw.imagenes
        .filter((img: { url: string }) => img.url?.trim())
        .map((img: any) => ({
          id: img.id,
          url: img.url.trim(),
        })),
    };

    const id = this.route.snapshot.paramMap.get('id');
    const isDocente = this.router.url.includes('docentes');

    if (id) {
      this.PlantasServicio.actualizarPlanta(+id, payload).subscribe({
        next: () => {
          this.submitStatus = 'success';
          alert('Planta actualizada exitosamente');
          this.redirigir(isDocente);
        },
        error: (err) => this.manejarError(err),
      });
    } else {
      this.PlantasServicio.crearPlanta(payload).subscribe({
        next: () => {
          this.submitStatus = 'success';
          alert('Planta guardada exitosamente');
          this.redirigir(isDocente);
        },
        error: (err) => this.manejarError(err),
      });
    }
  }

  private redirigir(isDocente: boolean): void {
    if (isDocente) {
      this.router.navigate(['/docentes']);
    } else {
      this.router.navigate(['/admin/plantas']);
    }
  }

  private manejarError(err: any): void {
    this.submitStatus = 'error';
    this.errorMessage = err?.error?.detail ?? 'Ocurrió un error al guardar la planta.';
    alert(this.errorMessage);
  }

  hasError(field: string, error: string): boolean {
    const ctrl = this.form.get(field);
    return !!(ctrl?.hasError(error) && (ctrl.dirty || ctrl.touched));
  }

  onReset(): void {
    this.form.reset();
    this.imagenes.clear();
    this.imagenes.push(this.createImagenControl());
    this.submitStatus = 'idle';
    this.errorMessage = '';

    if (this.esDocente) {
      this.router.navigate(['/docentes']);
    } else {
      this.router.navigate(['/admin/plantas']);
    }
  }

  get esDocente(): boolean {
    return this.router.url.includes('/docentes');
  }
}
