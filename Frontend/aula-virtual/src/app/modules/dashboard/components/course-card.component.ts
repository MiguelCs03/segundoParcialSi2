import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-course-card',
  imports: [CommonModule],
  template: `
    <div class="bg-white shadow-md rounded-xl p-4 border border-slate-200 hover:shadow-lg transition">
      <h2 class="text-xl font-semibold text-slate-800 mb-2">{{ curso }}</h2>

      <div class="flex flex-col gap-2 mb-4">
        <p class="text-sm text-gray-600">Promedio del curso: <span class="font-bold text-blue-700">82.4</span></p>
        <p class="text-sm text-gray-600">Predicción rendimiento: <span class="font-bold text-green-600">Alto</span></p>
      </div>

      <button
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
        (click)="verDetalles()">
        Ver Detalles
      </button>
    </div>
  `
})
export class CourseCardComponent {
  @Input() curso: string = '';
  @Input() detalleMateriaId!: number;

  @Output() detalleClick = new EventEmitter<number>();

  verDetalles() {
    this.detalleClick.emit(this.detalleMateriaId);
  }
}
