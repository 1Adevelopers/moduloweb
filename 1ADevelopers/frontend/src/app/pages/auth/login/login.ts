import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../services/auth';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrls: ['./login.css'],
})
export class IniciarSesionComponent {
  form: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private authService: AuthService
  ) {
    this.form = this.formBuilder.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  iniciarSesion() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const credentials = {
      email: this.form.value.email,
      password: this.form.value.password,
    };

    this.authService.login(credentials).subscribe({
      next: (response) => {
        const user = response.user;
        
        alert(`¡Bienvenido a FlorApp, ${user.nombre}!`);
        localStorage.setItem('user', JSON.stringify(user));
      
        const idRol = Number(user.rol);

        if (user.rol === 1) {
          this.router.navigate(['/admin']);
        } else if (user.rol === 2) {
          this.router.navigate(['/docentes']);
        } else {
          this.router.navigate(['/home']);

        }
        },
        error: (err) => {
        console.error(err);
        alert('Correo o contraseña incorrectos');
      }

    });
  }
}