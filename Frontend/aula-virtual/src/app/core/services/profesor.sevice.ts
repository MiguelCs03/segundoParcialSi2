import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ProfesorService {
  private apiUrl = 'http://127.0.0.1:8000/api/profesor/materias/';

  constructor(private http: HttpClient) {}

  getMateriasConCurso(): Observable<any[]> {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<any[]>(this.apiUrl, { headers });
  }

  getEstudiantesDeMateria(detalleId: number): Observable<any[]> {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.get<any[]>(`http://127.0.0.1:8000/api/profesor/materia/${detalleId}/estudiantes/`, { headers });
  }

  registrarAsistencia(detalleId: number, asistencias: any[]): Observable<any> {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
    return this.http.post(`http://127.0.0.1:8000/api/profesor/materia/${detalleId}/registrar-asistencia/`, asistencias, { headers });
  }

  obtenerAsistenciaPorFecha(detalleId: number, fecha?: string): Observable<any> {
    const token = localStorage.getItem('access_token');
    const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);

    let url = `http://127.0.0.1:8000/api/profesor/materia/${detalleId}/asistencia-por-fecha/`;
    if (fecha) {
      url += `?fecha=${fecha}`;
    }
    return this.http.get<any>(url, { headers });
  }

  obtenerReporteAsistencia(detalleId: number) {
   const token = localStorage.getItem('access_token');
   const headers = new HttpHeaders().set('Authorization', `Bearer ${token}`);
   return this.http.get<any>(`http://127.0.0.1:8000/api/profesor/materia/${detalleId}/reporte-asistencia/`, { headers });
  }


}
