import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { SidebarComponent } from '../components/sidebar.component';
import { NgIf, NgFor } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-materia-detalle',
  imports: [CommonModule, HttpClientModule, SidebarComponent, NgIf, NgFor],
  template: `
    <div class="flex min-h-screen">
      <app-sidebar></app-sidebar>
      <div class="flex-1 p-6 bg-gray-50">
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold text-slate-800">Detalle de la Materia</h1>
          <button
            class="text-sm px-3 py-1 border rounded text-blue-600 border-blue-600 hover:bg-blue-100"
            (click)="volver()"
          >
            ← Volver
          </button>
        </div>

        <p class="text-gray-600 mb-4">ID del detalle materia: <strong>{{ detalleId }}</strong></p>

        <div class="bg-white rounded shadow overflow-hidden">
          <table class="w-full text-left table-auto">
            <thead class="bg-gray-100 text-slate-700 font-semibold">
              <tr>
                <th class="p-3">Nombre</th>
                <th class="p-3">ID</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let est of estudiantes" class="border-b hover:bg-gray-50">
                <td class="p-3">{{ est.nombre }}</td>
                <td class="p-3">{{ est.id }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `
})
export class MateriaDetalleComponent implements OnInit {
  detalleId!: number;
  estudiantes: any[] = [];

  constructor(private route: ActivatedRoute, private http: HttpClient) {}

  ngOnInit(): void {
    this.detalleId = +this.route.snapshot.paramMap.get('id')!;
    this.cargarEstudiantes();
  }

  cargarEstudiantes() {
    const token = localStorage.getItem('access_token');
    const headers = { Authorization: `Bearer ${token}` };

    this.http
      .get<any[]>(`http://127.0.0.1:8000/api/profesor/materia/${this.detalleId}/estudiantes/`, { headers })
      .subscribe({
        next: (data) => {
          this.estudiantes = data;
        },
        error: (err) => {
          console.error('Error al obtener estudiantes:', err);
        }
      });
  }

  volver() {
    window.history.back(); // o this.router.navigate(['/profesor']);
  }
}
