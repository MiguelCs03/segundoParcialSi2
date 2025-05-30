import { Component, OnInit } from '@angular/core';
import { NgIf, NgFor, NgClass } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TutorService } from '../../../core/services/tutor.service';
import { SidebarComponent } from '../components/sidebar.component';

@Component({
  selector: 'app-tutor-dashboard',
  standalone: true,
  imports: [NgIf, NgFor, NgClass, FormsModule, SidebarComponent],
  template: `
    <div class="flex min-h-screen">

      <!-- Sidebar -->
      <app-sidebar class="w-64"></app-sidebar>

      <!-- Contenido principal -->
      <main class="flex-1 p-6 bg-gray-100 overflow-auto">

        <h1 class="text-3xl font-bold mb-6">Dashboard Tutor</h1>

        <!-- Selección de hijo -->
        <div *ngIf="estudiantes.length > 0" class="mb-8">
          <label for="select-hijo" class="block mb-2 font-semibold">Selecciona a tu hijo:</label>
          <select
            id="select-hijo"
            class="border border-gray-300 rounded p-2 w-full max-w-xs"
            [(ngModel)]="hijoSeleccionado"
            (change)="cargarDatosHijo()"
          >
            <option *ngFor="let estudiante of estudiantes" [value]="estudiante.id">
              {{ estudiante.nombre }} (Código: {{ estudiante.codigo }})
            </option>
          </select>
        </div>

        <!-- Resumen del hijo seleccionado -->
        <div *ngIf="hijoDatos" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div class="bg-white p-4 rounded shadow">
            <p class="text-gray-500">Promedio general</p>
            <p class="text-2xl font-bold text-blue-600">{{ hijoDatos.promedio || 'N/A' }}</p>
          </div>
          <div class="bg-white p-4 rounded shadow">
            <p class="text-gray-500">Asistencia</p>
            <p class="text-2xl font-bold text-green-600">{{ hijoDatos.asistencia || 'N/A' }}%</p>
          </div>
          <div class="bg-white p-4 rounded shadow">
            <p class="text-gray-500">Participación</p>
            <p class="text-2xl font-bold text-yellow-500">{{ hijoDatos.participacion || 'N/A' }}%</p>
          </div>
          <div class="bg-white p-4 rounded shadow">
            <p class="text-gray-500">Predicción</p>
            <p class="text-2xl font-bold text-purple-600">{{ hijoDatos.prediccion || 'N/A' }}</p>
          </div>
        </div>

        <!-- Materias actuales del hijo -->
        <div *ngIf="hijoMaterias?.length" class="mb-8">
          <h2 class="text-xl font-semibold mb-4">Materias actuales</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div *ngFor="let materia of hijoMaterias" class="bg-white p-4 rounded shadow">
              <p class="font-bold text-lg">{{ materia.nombre }}</p>
              <p class="text-sm text-gray-600">Profesor: {{ materia.profesor }}</p>
              <p class="text-sm">Promedio: <span class="text-blue-600 font-semibold">{{ materia.promedio || 'N/A' }}</span></p>
            </div>
          </div>
        </div>

        <!-- Actividades recientes -->
        <div *ngIf="hijoActividades?.length" class="bg-white p-4 rounded shadow">
          <h2 class="text-xl font-semibold mb-4">Actividades recientes</h2>
          <table class="w-full table-auto">
            <thead>
              <tr class="border-b text-left">
                <th class="py-2">Materia</th>
                <th>Título</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let actividad of hijoActividades" class="border-b hover:bg-gray-50">
                <td class="py-2">{{ actividad.materia }}</td>
                <td>{{ actividad.titulo }}</td>
                <td>
                  <span [ngClass]="{
                    'text-green-600': actividad.estado === 'Entregado',
                    'text-yellow-500': actividad.estado === 'Pendiente'
                  }">{{ actividad.estado }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

      </main>
    </div>
  `
})
export class TutorDashboardComponent implements OnInit {

  estudiantes: any[] = [];
  hijoSeleccionado: number | null = null;

  hijoDatos: any = null;
  hijoMaterias: any[] = [];
  hijoActividades: any[] = [];

  constructor(private tutorService: TutorService) {}

  ngOnInit() {
    this.tutorService.getEstudiantes().subscribe({
      next: (data) => {
        this.estudiantes = data;
        if (data.length > 0) {
          this.hijoSeleccionado = data[0].id;
          this.cargarDatosHijo();
        }
      },
      error: (err) => console.error('Error cargando estudiantes', err)
    });
  }

  cargarDatosHijo() {
    if (!this.hijoSeleccionado) return;

    // Aquí debes implementar llamadas al backend para traer datos reales de:
    // resumen, materias y actividades del hijo seleccionado.
    // Por ahora, simulo con datos estáticos:

    this.hijoDatos = {
      promedio: 85,
      asistencia: 95,
      participacion: 80,
      prediccion: 'Alto'
    };

    this.hijoMaterias = [
      { nombre: 'Matemáticas', profesor: 'prof alex', promedio: 86 },
      { nombre: 'Lenguaje', profesor: 'profina maria', promedio: 90 },
      { nombre: 'Historia', profesor: 'prof juan', promedio: 85 }
    ];

    this.hijoActividades = [
      { materia: 'Matemáticas', titulo: 'Ejercicios algebra', estado: 'Pendiente' },
      { materia: 'Lenguaje', titulo: 'Ensayo literario', estado: 'Entregado' },
      { materia: 'Historia', titulo: 'Línea de tiempo', estado: 'Pendiente' }
    ];
  }
}
