import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { QuienesSomos } from './pages/quienes-somos/quienes-somos';
import { Contact } from './pages/contact/contact';
import { Notfound404 } from './pages/notfound404/notfound404';
import { Enproceso } from './shared/enproceso/enproceso';
import { Dashboard } from './pages/dashboard/dashboard';
import { PlantList } from './pages/plants/plant-list/plant-list';
import { UserList } from './pages/users/user-list/user-list';
import { UserForm } from './pages/users/user-form/user-form';
import { IniciarSesionComponent } from './pages/auth/login/login';
import { Galeriafichas } from './pages/galeriafichas/galeriafichas';
import { DocenteDashboard } from './pages/docentes/docente-dashboard/docente-dashboard';
import { PlantForm } from './pages/plants/plant-form/plant-form';
import { RegisterComponent } from './pages/auth/register/register';
import { MensajesLista } from './pages/mensajes-lista/mensajes-lista';
import { adminGuard } from './guards/admin.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: Home },
  { path: 'login', component: IniciarSesionComponent },
  { path: 'register', component: RegisterComponent },
  {
    path: 'admin',
    component: Dashboard,
    canActivate: [adminGuard],
    children: [
      { path: 'plantas', component: PlantList },
      { path: 'nueva-planta', component: PlantForm },
      { path: 'editar-planta/:id', component: PlantForm },
      { path: 'usuarios', component: UserList },
      { path: 'usuarios/nuevo', component: UserForm },
      { path: 'usuarios/editar/:id', component: UserForm },
      { path: 'mensajes', component: MensajesLista },
    ],
  },

  { path: 'docentes', component: DocenteDashboard },
  { path: 'docentes/nueva-planta', component: PlantForm },
  { path: 'docentes/editar-planta/:id', component: PlantForm },

  { path: 'quienes-somos', component: QuienesSomos },
  { path: 'galeria', component: Galeriafichas },
  { path: 'contacto', component: Contact },
  { path: '**', component: Notfound404 },
];
