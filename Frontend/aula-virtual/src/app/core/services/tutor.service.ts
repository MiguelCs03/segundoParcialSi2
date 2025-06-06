import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TutorService {
  private baseUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
  }

  // ✅ Obtener lista de estudiantes hijos (endpoint original)
  getEstudiantes(): Observable<any[]> {
    const headers = this.getHeaders();
    return this.http.get<any[]>(`${this.baseUrl}/tutor/estudiantes/`, { headers });
  }

  // ✅ Obtener resumen general de un hijo (nuevo endpoint)
  getResumenHijo(estudianteId: number): Observable<any> {
    const headers = this.getHeaders();
    return this.http.get<any>(`${this.baseUrl}/tutor/hijo/${estudianteId}/resumen/`, { headers });
  }

  // ✅ Obtener rendimiento detallado (nuevo endpoint)
  getRendimientoDetallado(estudianteId: number): Observable<any> {
    const headers = this.getHeaders();
    return this.http.get<any>(`${this.baseUrl}/tutor/hijo/${estudianteId}/rendimiento/`, { headers });
  }
}
