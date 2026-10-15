import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Contacto } from '../interfaces/contacto';

@Injectable({
  providedIn: 'root',
})
export class ContactoService {
  private apiUrl = 'http://localhost:8000/api/interacciones/';

  constructor(private http: HttpClient) {}

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: token ? `Bearer ${token}` : '',
    });
  }

  getMensajes(): Observable<Contacto[]> {
    return this.http.get<Contacto[]>(this.apiUrl, { headers: this.getAuthHeaders() });
  }

  marcarLeido(id: number): Observable<Contacto> {
    return this.http.patch<Contacto>(
      `${this.apiUrl}${id}/marcar-leido/`,
      {},
      { headers: this.getAuthHeaders() },
    );
  }

  marcarRespondido(id: number): Observable<Contacto> {
    return this.http.patch<Contacto>(
      `${this.apiUrl}${id}/marcar-respondido/`,
      {},
      { headers: this.getAuthHeaders() },
    );
  }
}
