import { Component, Input, OnInit } from '@angular/core';
import { LoginService } from '../../services/login.service';
import { MatButtonModule } from '@angular/material/button';
import { EMPTY, Observable, concatMap, finalize, from, of } from 'rxjs';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-facebook-login',
  standalone: true,
  imports: [MatButtonModule, CommonModule, MatIconModule],
  templateUrl: './facebook-login.component.html',
  styleUrl: './facebook-login.component.scss'
})
export class FacebookLoginComponent {
  @Input() loggedIn!: boolean;

  inProgress = false;
  constructor(private loginService: LoginService){}

  login() {
    this.inProgress = true;
    const win = window as typeof window & typeof globalThis & { opera: string, MSStream:unknown};
    const userAgent = navigator.userAgent || navigator.vendor || win.opera;

    if (/android/i.test(userAgent)) {
      window.location.href = 'intent://' + environment.deepLink + '#Intent;package=com.facebook.katana;scheme=fb;end';
    } else if (/iPad|iPhone|iPod/.test(userAgent) && !win.MSStream) {
        window.location.href = 'fb://profile/' + environment.deepLink;
    } else {
      this.facebookLogin().pipe(concatMap(accessToken => this.loginService.apiAuthenticate(accessToken ?? '')), finalize(() => this.inProgress = false)).subscribe((jwt) => {
        localStorage.setItem('jwt', jwt.access_token);
        localStorage.setItem('refresh', jwt.refresh_token);
        this.loginService.updateStatus(true);
      });
    }
  }

  facebookLogin(): Observable<string | undefined> {
      return from(new Promise<fb.StatusResponse>(resolve => FB.login(resolve, {scope: 'email'}))).pipe(concatMap(({ authResponse }) => {
        if (!authResponse){
            return EMPTY;
        };
        return of(authResponse.accessToken);
      }));
  }

  logout() {
    this.loginService.logout();
}
}
