import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ProfesorService } from '../../../core/services/profesor.sevice';
import { CommonModule, NgFor, NgIf } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-asistencia',
  imports: [CommonModule, FormsModule, NgFor, NgIf],
  template: `
    <nav class="bg-indigo-600 p-4 text-white flex justify-between items-center">
      <button (click)="volver()" class="hover:bg-indigo-700 px-3 py-1 rounded">
        ← Volver
      </button>
      <h1 class="text-lg font-semibold">Tomar Asistencia</h1>
      <div></div>
    </nav>

    <div class="max-w-3xl mx-auto p-6 bg-white rounded shadow mt-6">

      <!-- NUEVO: Mostrar formulario o tabla según si ya se tomó asistencia -->
      <ng-container *ngIf="!asistenciasRegistradas; else mostrarAsistencias">
        <form (submit)="guardarAsistencia(); $event.preventDefault()" class="space-y-4">
          <div *ngFor="let estudiante of estudiantes; let i = index" class="flex items-center justify-between border-b py-2">
            <span>{{ estudiante.nombre }}</span>
            <input type="checkbox"
                   [(ngModel)]="asistencias[i].presente"
                   name="asistencia_{{i}}"
                   class="w-6 h-6 text-indigo-600" />
          </div>
          <button type="submit" class="bg-indigo-600 text-white rounded px-4 py-2 hover:bg-indigo-700">
            Guardar Asistencia
          </button>
        </form>
      </ng-container>

      <!-- NUEVO: Template para mostrar asistencias ya tomadas -->
      <ng-template #mostrarAsistencias>
        <h2 class="text-xl mb-4">Asistencia tomada el {{ fechaAsistencia }}</h2>
        <table class="w-full text-left table-auto border rounded">
          <thead class="bg-gray-100 font-semibold">
            <tr>
              <th class="p-2 border">Estudiante</th>
              <th class="p-2 border">Presente</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let asistencia of asistenciasExistentes" class="border-b">
              <td class="p-2 border">{{ asistencia.nombre }}</td>
              <td class="p-2 border text-center">
                <input type="checkbox" [checked]="asistencia.presente" disabled />
              </td>
            </tr>
          </tbody>
        </table>
      </ng-template>

    </div>
  `,
})
export default class AsistenciaComponent implements OnInit {
  detalleId!: number;
  estudiantes: any[] = [];
  asistencias: { libreta_id: number; presente: boolean }[] = [];

  // NUEVO: variables para control de asistencias ya tomadas
  asistenciasRegistradas = false;
  fechaAsistencia = '';
  asistenciasExistentes: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private profesorService: ProfesorService
  ) {}

  ngOnInit(): void {
    this.detalleId = Number(this.route.snapshot.paramMap.get('id'));

    // NUEVO: Consultar si ya hay asistencias tomadas hoy
    this.profesorService.obtenerAsistenciaPorFecha(this.detalleId).subscribe({
      next: (res) => {
        if (res.asistencias && res.asistencias.length > 0) {
          this.asistenciasRegistradas = true;
          this.fechaAsistencia = res.fecha;
          this.asistenciasExistentes = res.asistencias;
        } else {
          this.cargarEstudiantesParaAsistencia();
        }
      },
      error: (err) => {
        console.error(err);
        this.cargarEstudiantesParaAsistencia();
      }
    });
  }

  // NUEVO: carga estudiantes para mostrar el formulario
  cargarEstudiantesParaAsistencia(): void {
    this.profesorService.getEstudiantesDeMateria(this.detalleId).subscribe(data => {
      this.estudiantes = data;
      this.asistencias = data.map((e: any) => ({
        libreta_id: e.libreta_id,
        presente: false,
      }));
    });
  }

  guardarAsistencia(): void {
    this.profesorService.registrarAsistencia(this.detalleId, this.asistencias).subscribe({
      next: () => alert('Asistencia guardada correctamente'),
      error: err => console.error(err)
    });
  }

  volver(): void {
    window.history.back();
  }
}
