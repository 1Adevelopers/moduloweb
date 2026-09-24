import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';


@Injectable({
  providedIn: 'root',
})

export class AuthService {
  private baseUrl = 'http://127.0.0.1:8000/api/';
  
  constructor(private http: HttpClient) {}


 // REGISTRO 
  register(userData: any): Observable<any> {
  return this.http.post(`${this.baseUrl}usuarios/`, userData);
}


 // LOGIN
  login(credentials: { email: string; contrasena: string }): Observable<any> {
  return this.http.post<{ access: string; refresh: string}>(`${this.baseUrl}token/`, credentials).pipe(
    tap((tokens) => {
      localStorage.setItem('access_token', tokens.access);
      localStorage.setItem('refresh_token', tokens.refresh);
    })
  );
}
}
