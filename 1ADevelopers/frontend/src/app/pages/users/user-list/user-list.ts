import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { UsuarioService } from '../../../services/usuario';
import { Usuario } from '../../../interfaces/usuario';

@Component({
  selector: 'app-user-list',
  imports: [RouterModule, CommonModule],
  templateUrl: './user-list.html',
  styleUrl: './user-list.css',
})
export class UserList implements OnInit {
  private usuarioService = inject(UsuarioService);
  private cdr = inject(ChangeDetectorRef);

  usuarios: Usuario[] = [];

  ngOnInit(): void {
    this.cargarUsuarios();
  }

  cargarUsuarios(): void {
    this.usuarioService.ObtenerUsuarios().subscribe({
      next: (data) => {
        console.log('Usuarios cargados desde el backend:', data);
        this.usuarios = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error al cargar usuarios:', err)
      }
    });
  }
  
  
  eliminarUsuario(id: number | undefined): void {
    if (id && confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
      this.usuarioService.eliminarUsuario(id).subscribe({
        next: () => {
          alert('Usuario eliminado con éxito');
          this.cargarUsuarios();
        },
        error: (err) => console.error('Error al eliminar usuario:', err)
      });
    }
  }
}

