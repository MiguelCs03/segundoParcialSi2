import { Component } from '@angular/core';
import { NgFor, NgClass, NgIf } from '@angular/common';


@Component({
  selector: 'app-alumno-dashboard',
  standalone: true,
 imports: [NgFor, NgClass, NgIf],
  template: `
    <div class="min-h-screen p-6 bg-gradient-to-b from-blue-100 to-blue-300">

      <h2 class="text-2xl font-bold mb-6">Bienvenido, Alumno</h2>

      <!-- Resumen -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-white p-4 rounded shadow">
          <p class="text-gray-500">Promedio actual</p>
          <p class="text-2xl font-bold text-blue-600">{{ resumen.promedio }}</p>
        </div>
        <div class="bg-white p-4 rounded shadow">
          <p class="text-gray-500">Asistencia</p>
          <p class="text-2xl font-bold text-green-600">{{ resumen.asistencia }}%</p>
        </div>
        <div class="bg-white p-4 rounded shadow">
          <p class="text-gray-500">Participación</p>
          <p class="text-2xl font-bold text-yellow-500">{{ resumen.participacion }}%</p>
        </div>
        <div class="bg-white p-4 rounded shadow">
          <p class="text-gray-500">Predicción</p>
          <p class="text-2xl font-bold text-purple-600">{{ resumen.prediccion }}</p>
        </div>
      </div>

      <!-- Materias -->
      <h3 class="text-xl font-semibold mb-2">Materias actuales</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div *ngFor="let materia of materias" class="bg-white p-4 rounded shadow">
          <p class="text-lg font-bold">{{ materia.nombre }}</p>
          <p class="text-sm text-gray-500">Profesor: {{ materia.profesor }}</p>
          <p class="text-sm">Promedio: <span class="text-blue-600 font-semibold">{{ materia.promedio }}</span></p>
          <button class="mt-3 bg-blue-600 hover:bg-blue-700 text-white px-4 py-1 rounded">Ver Detalles</button>
        </div>
      </div>

      <!-- Actividades -->
      <h3 class="text-xl font-semibold mb-2">Actividades recientes</h3>
      <div class="bg-white rounded shadow p-4">
        <table class="w-full table-auto">
          <thead>
            <tr class="text-left border-b">
              <th class="py-2">Materia</th>
              <th>Título</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let actividad of actividades" class="border-b hover:bg-gray-50">
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
    </div>
  `,
})
export class AlumnoDashboardComponent {

  resumen = {
    promedio: 84.5,
    asistencia: 92,
    participacion: 87,
    prediccion: 'Alto'
  };

  materias = [
    { nombre: 'Matemáticas', promedio: 85.2, profesor: 'Lic. Pérez' },
    { nombre: 'Lenguaje', promedio: 82.1, profesor: 'Lic. Gutiérrez' },
    { nombre: 'Historia', promedio: 79.8, profesor: 'Lic. Romero' }
  ];

  actividades = [
    { materia: 'Matemáticas', titulo: 'Ejercicios de álgebra', estado: 'Pendiente' },
    { materia: 'Lenguaje', titulo: 'Ensayo literario', estado: 'Entregado' },
    { materia: 'Historia', titulo: 'Línea de tiempo', estado: 'Pendiente' }
  ];

}
