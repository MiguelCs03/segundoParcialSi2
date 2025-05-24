import { Injectable, signal } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs/operators';


export interface Usuario {
  id: number;
  nombre: string;
  codigo: string;
  rol: { nombre: 'admin' | 'profesor' | 'estudiante' | 'tutor' };
  [key: string]: any;
}

@Injectable({ providedIn: 'root' })
export class SessionService {
  private usuario = signal<Usuario | null>(null);
  private readonly storageKey = 'usuario';

  constructor(private router: Router, private http: HttpClient) {
   if (typeof localStorage !== 'undefined') {
  const data = localStorage.getItem(this.storageKey);
  if (data) this.usuario.set(JSON.parse(data));
    }
  }

  login(codigo: string, password: string) {
  return this.http.post<{ detail: string; usuario: Usuario }>('http://127.0.0.1:8000/api/login/', { codigo, password }).pipe(
    tap((resp) => {
      this.setUsuario(resp.usuario);
      this.redireccionarPorRol(resp.usuario.rol?.nombre);
    })
  );
 }


  private redireccionarPorRol(rol: string) {
    switch (rol) {
      case 'admin':
        this.router.navigate(['/admin']);
        break;
      case 'profesor':
        this.router.navigate(['/profesor']);
        break;
      case 'estudiante':
        this.router.navigate(['/mi-rendimiento']);
        break;
      case 'tutor':
        this.router.navigate(['/mi-hijo']);
        break;
      default:
        this.router.navigate(['/']);
    }
  }

  setUsuario(usuario: Usuario) {
  this.usuario.set(usuario);
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem(this.storageKey, JSON.stringify(usuario));
  }
}

logout() {
  this.usuario.set(null);
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem(this.storageKey);
  }
  this.router.navigate(['/login']);
}


  get currentUser() {
    return this.usuario();
  }

  get role() {
    return this.usuario()?.rol?.nombre;
  }

  get isLoggedIn() {
    return !!this.usuario();
  }
}
