import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../components/sidebar.component';
import { CourseCardComponent } from '../components/course-card.component';
import { ProfesorService } from '../../../core/services/profesor.sevice';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-profesor-dashboard',
  imports: [CommonModule, SidebarComponent, CourseCardComponent],
  template: `
    <div class="flex min-h-screen">
      <app-sidebar></app-sidebar>
      <div class="flex-1 p-6">
        <h1 class="text-2xl font-bold mb-4">Bienvenido, Profesor</h1>

        <div class="flex gap-4 mb-6">
          <button class="bg-blue-700 text-white px-4 py-2 rounded">Nueva Tarea</button>
          <button class="border border-blue-700 text-blue-700 px-4 py-2 rounded">Gestionar Alumnos</button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <app-course-card
            *ngFor="let m of materias"
            [curso]="m.materia + ' - ' + m.curso + ' ' + m.paralelo"
            [detalleMateriaId]="m.detalle_id"
            (detalleClick)="irADetalle(m.detalle_id)">
          </app-course-card>
        </div>
      </div>
    </div>
  `
})
export class ProfesorDashboardComponent implements OnInit {
  materias: any[] = [];

  constructor(
    private profesorService: ProfesorService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.profesorService.getMateriasConCurso().subscribe(data => {
      this.materias = data;
    });
  }

  irADetalle(id: number) {
    this.router.navigate(['/profesor/materia', id]);
  }
}
