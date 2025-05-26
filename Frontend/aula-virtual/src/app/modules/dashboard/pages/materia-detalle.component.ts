import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-materia-detalle',
  imports: [CommonModule],
  template: `
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">Detalle de la Materia</h1>
      <p class="text-gray-700 mb-2">ID del detalle materia: <strong>{{ detalleId }}</strong></p>

      <div class="mt-6">
        <!-- Aquí luego mostraremos notas, asistencia, tareas, etc -->
        <p class="text-gray-500">Contenido en desarrollo...</p>
      </div>
    </div>
  `
})
export class MateriaDetalleComponent implements OnInit {
  detalleId!: number;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.detalleId = +this.route.snapshot.paramMap.get('id')!;
  }
}
