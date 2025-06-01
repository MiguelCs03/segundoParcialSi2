import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';  // Importa Router
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  standalone: true,
  selector: 'app-reporte-entregas',
  imports: [CommonModule, HttpClientModule],
  template: `
    <div class="p-6 overflow-auto max-w-full">
      <button
        (click)="volver()"
        class="mb-4 px-4 py-2 border rounded hover:bg-gray-100"
      >
        ← Volver
      </button>

      <table class="table-auto border-collapse border border-gray-300 w-full">
        <thead>
          <tr>
            <th class="border border-gray-300 p-2 sticky top-0 bg-white">Estudiante</th>
            <th *ngFor="let act of actividades" class="border border-gray-300 p-2 sticky top-0 bg-white">
              {{ act }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let est of estudiantes">
            <td class="border border-gray-300 p-2">{{ est.nombre }}</td>
            <td *ngFor="let ent of est.entregas" class="border border-gray-300 p-2 whitespace-normal">
              <div *ngIf="ent.entregado">
                ✓ {{ ent.calificacion }}<br />
                <small>{{ ent.fecha_entrega }}</small>
              </div>
              <div *ngIf="!ent.entregado" class="text-red-600 font-semibold">✗ No entregado</div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  `
})
export class ReporteEntregasComponent implements OnInit {
  detalleId!: number;
  estudiantes: any[] = [];
  actividades: string[] = [];

  constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.detalleId = +this.route.snapshot.paramMap.get('id')!;
    const token = localStorage.getItem('access_token');
    const headers = { Authorization: `Bearer ${token}` };

    this.http
      .get<any>(`http://127.0.0.1:8000/api/profesor/materia/${this.detalleId}/reporte-entregas/`, { headers })
      .subscribe(data => {
        this.estudiantes = data.estudiantes;
        this.actividades = data.actividades;
      });
  }

  volver() {
    this.router.navigate(['/profesor/materia', this.detalleId]);
  }
}
