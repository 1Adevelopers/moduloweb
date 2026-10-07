import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Categoria } from '../interfaces/categoria';
import { Especie } from '../interfaces/especie';

@Injectable({ providedIn: 'root' })
export class PlantasServicio {
  private http = inject(HttpClient);
  private API = 'http://localhost:8000/api/flora';

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: token ? `Bearer ${token}` : '',
    });
  }

  getMisPlantas(usuarioId: number): Observable<Especie[]> {
    return this.http.get<Especie[]>(`${this.API}/especies/mis-especies/?usuario_id=${usuarioId}`, {
      headers: this.getAuthHeaders(),
    });
  }

  getCategorias(): Observable<Categoria[]> {
    return this.http.get<Categoria[]>(`${this.API}/categorias/`, {
      headers: this.getAuthHeaders(),
    });
  }

  getPlantas(): Observable<Especie[]> {
    return this.http.get<Especie[]>(`${this.API}/especies/`, {
      headers: this.getAuthHeaders(),
    });
  }

  crearPlanta(especie: Especie): Observable<Especie> {
    return this.http.post<Especie>(`${this.API}/especies/`, especie, {
      headers: this.getAuthHeaders(),
    });
  }

  eliminarPlanta(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API}/especies/${id}/`, {
      headers: this.getAuthHeaders(),
    });
  }

  actualizarPlanta(id: number, especie: Especie): Observable<any> {
    return this.http.put<any>(`${this.API}/especies/${id}/`, especie, {
      headers: this.getAuthHeaders(),
    });
  }

  getPlantaId(id: number): Observable<Especie> {
    return this.http.get<Especie>(`${this.API}/especies/${id}/`, {
      headers: this.getAuthHeaders(),
    });
  }
}
