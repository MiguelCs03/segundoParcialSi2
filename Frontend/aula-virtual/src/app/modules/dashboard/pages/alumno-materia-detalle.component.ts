import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgFor, NgClass, NgIf, DatePipe } from '@angular/common'; // 👈 Agregar DatePipe
import { AlumnoService } from '../../../core/services/alumno.service';
import { SidebarComponent } from '../components/sidebar.component';

@Component({
  selector: 'app-alumno-materia-detalle',
  standalone: true,
  imports: [NgFor, NgClass, NgIf, SidebarComponent], // 👈 Agregar DatePipe
  template: `
    <div class="flex min-h-screen">
      <!-- Sidebar -->
      <app-sidebar class="w-64"></app-sidebar>

      <!-- Contenido principal -->
      <main class="flex-1 p-6 bg-gradient-to-b from-blue-100 to-blue-300 overflow-auto">
        
        <!-- Header con botón de regreso -->
        <div class="flex items-center justify-between mb-6">
          <div>
            <button 
              (click)="volver()" 
              class="flex items-center text-blue-600 hover:text-blue-800 mb-2">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
              Volver al Dashboard
            </button>
            <h1 class="text-3xl font-bold text-gray-800">{{ detalleMateria.nombre || 'Cargando...' }}</h1>
          </div>
        </div>

        <!-- Loading -->
        <div *ngIf="cargando" class="flex justify-center items-center my-10">
          <div class="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500"></div>
        </div>

        <!-- Error -->
        <div *ngIf="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
          <p>{{ error }}</p>
        </div>

        <!-- Contenido principal -->
        <div *ngIf="!cargando && !error">
          
          <!-- 1. Información General -->
          <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-2xl font-semibold mb-4 text-gray-800">Información General</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p class="text-gray-600 font-medium">Materia:</p>
                <p class="text-lg font-semibold">{{ detalleMateria.nombre }}</p>
              </div>
              <div>
                <p class="text-gray-600 font-medium">Profesor:</p>
                <p class="text-lg font-semibold">{{ detalleMateria.profesor }}</p>
              </div>
              <div>
                <p class="text-gray-600 font-medium">Promedio General:</p>
                <p class="text-2xl font-bold text-blue-600">{{ detalleMateria.promedio }}</p>
              </div>
            </div>
          </div>

          <!-- 2. Lista de Actividades -->
          <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-2xl font-semibold mb-4 text-gray-800">Actividades Asignadas</h2>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Título</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha Entrega</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nota</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr *ngFor="let actividad of actividades" class="hover:bg-gray-50">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {{ actividad.titulo }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {{ formatearFecha(actividad.fecha_entrega) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                            [ngClass]="{
                              'bg-green-100 text-green-800': actividad.estado === 'Entregado',
                              'bg-yellow-100 text-yellow-800': actividad.estado === 'Pendiente',
                              'bg-red-100 text-red-800': actividad.estado === 'Vencido'
                            }">
                        {{ actividad.estado }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <span *ngIf="actividad.nota !== null" class="font-semibold"
                            [ngClass]="{
                              'text-green-600': actividad.nota >= 80,
                              'text-yellow-600': actividad.nota >= 60 && actividad.nota < 80,
                              'text-red-600': actividad.nota < 60
                            }">
                        {{ actividad.nota }}
                      </span>
                      <span *ngIf="actividad.nota === null" class="text-gray-400">Sin calificar</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- 3. Asistencia por Materia -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <!-- Resumen de Asistencia -->
            <div class="bg-white rounded-lg shadow p-6">
              <h2 class="text-2xl font-semibold mb-4 text-gray-800">Asistencia</h2>
              <div class="space-y-4">
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Total de clases:</span>
                  <span class="font-semibold text-lg">{{ asistencia.total_clases }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Clases asistidas:</span>
                  <span class="font-semibold text-lg text-green-600">{{ asistencia.clases_asistidas }}</span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-600">Clases perdidas:</span>
                  <span class="font-semibold text-lg text-red-600">{{ asistencia.clases_perdidas }}</span>
                </div>
                <div class="border-t pt-4">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-600 font-medium">Porcentaje de asistencia:</span>
                    <span class="text-2xl font-bold"
                          [ngClass]="{
                            'text-green-600': asistencia.porcentaje >= 80,
                            'text-yellow-600': asistencia.porcentaje >= 60 && asistencia.porcentaje < 80,
                            'text-red-600': asistencia.porcentaje < 60
                          }">
                      {{ asistencia.porcentaje }}%
                    </span>
                  </div>
                  <!-- Barra de progreso -->
                  <div class="w-full bg-gray-200 rounded-full h-3 mt-2">
                    <div class="h-3 rounded-full transition-all duration-300"
                         [style.width.%]="asistencia.porcentaje"
                         [ngClass]="{
                           'bg-green-500': asistencia.porcentaje >= 80,
                           'bg-yellow-500': asistencia.porcentaje >= 60 && asistencia.porcentaje < 80,
                           'bg-red-500': asistencia.porcentaje < 60
                         }">
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 4. Gráfico de Asistencia -->
            <div class="bg-white rounded-lg shadow p-6">
              <h2 class="text-2xl font-semibold mb-4 text-gray-800">Historial de Asistencia</h2>
              <div class="space-y-3">
                <div *ngFor="let dia of asistencia.historial_semanal" class="flex items-center">
                  <span class="w-20 text-sm text-gray-600">{{ dia.fecha }}</span>
                  <div class="flex-1 mx-4">
                    <div class="h-6 bg-gray-200 rounded-full relative">
                      <div class="h-6 rounded-full flex items-center justify-center text-white text-xs font-semibold transition-all duration-300"
                           [style.width]="dia.presente ? '100%' : '0%'"
                           [ngClass]="{
                             'bg-green-500': dia.presente,
                             'bg-red-500': !dia.presente
                           }">
                        {{ dia.presente ? 'Presente' : 'Ausente' }}
                      </div>
                    </div>
                  </div>
                  <span class="w-8 text-sm"
                        [ngClass]="{
                          'text-green-600': dia.presente,
                          'text-red-600': !dia.presente
                        }">
                    {{ dia.presente ? '✓' : '✗' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  `,
})
export class AlumnoMateriaDetalleComponent implements OnInit {
  materiaId!: number;
  cargando = true;
  error = '';

  detalleMateria: any = {
    nombre: '',
    profesor: '',
    promedio: 0
  };

  actividades: any[] = [];
  
  asistencia: any = {
    total_clases: 0,
    clases_asistidas: 0,
    clases_perdidas: 0,
    porcentaje: 0,
    historial_semanal: []
  };

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private alumnoService: AlumnoService
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.materiaId = +params['id'];
      this.cargarDatosMateria();
    });
  }

  // 👈 Agregar método para formatear fecha sin pipe
  formatearFecha(fechaISO: string): string {
    if (!fechaISO) return 'Sin fecha';
    
    try {
      const fecha = new Date(fechaISO);
      const dia = fecha.getDate().toString().padStart(2, '0');
      const mes = (fecha.getMonth() + 1).toString().padStart(2, '0');
      const año = fecha.getFullYear();
      return `${dia}/${mes}/${año}`;
    } catch (error) {
      return 'Fecha inválida';
    }
  }

  cargarDatosMateria(): void {
    this.cargando = true;
    this.error = '';

    // 👈 Usar el endpoint real que creamos
    this.alumnoService.getDetalleMateriaAlumno(this.materiaId).subscribe({
      next: (data) => {
        this.detalleMateria = data.materia;
        this.actividades = data.actividades;
        this.asistencia = data.asistencia;
        this.cargando = false;
      },
      error: (err) => {
        console.error('Error al cargar detalle de materia:', err);
        this.error = 'Error al cargar los datos de la materia';
        this.cargando = false;
      }
    });
  }

  volver(): void {
    this.router.navigate(['/mi-rendimiento']);
  }
}