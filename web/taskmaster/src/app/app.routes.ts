import { Routes } from '@angular/router';
import { TasksComponent } from './components/tasks/tasks.component';
import { ProfileComponent } from './components/profile/profile.component';
import { LoginCallbackComponent } from './components/login-callback/login-callback.component';

export const routes: Routes = [
    {path: '', title: 'Help It Done', component: TasksComponent},
    {
        path: 'profile',
        title: 'Help It Done - Profile',
        component: ProfileComponent,
    },
    {
        path: 'auth/fb-callback',
        title: 'Help It Done - Callback',
        component: LoginCallbackComponent,
    },
];
