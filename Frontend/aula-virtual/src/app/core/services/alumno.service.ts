import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AlumnoService {
  private apiUrl = 'http://127.0.0.1:8000/api'; // Cambia según tu backend

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token');  // Cambiado a 'access_token'
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  getMateriasPorAlumno(): Observable<any[]> {
    const headers = this.getHeaders();
    return this.http.get<any[]>(`${this.apiUrl}/alumno/materias/`, { headers });
  }

  getResumenDashboard(): Observable<any> {
  const token = localStorage.getItem('access_token');
  const headers = { Authorization: `Bearer ${token}` };
  return this.http.get<any>('http://127.0.0.1:8000/api/alumno/resumen/', { headers });
}

}
