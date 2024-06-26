import { Component, Input } from '@angular/core';
import { LoginService } from '../../services/login.service';
import { MatButtonModule } from '@angular/material/button';
import { EMPTY, Observable, concatMap, finalize, from, of } from 'rxjs';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { SnackBarService } from '../../services/snackBar.service';

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
  constructor(private loginService: LoginService, private snackBarService: SnackBarService){}

  login() {
    this.inProgress = true;
    this.facebookLogin().pipe(concatMap(accessToken => this.loginService.apiAuthenticate(accessToken ?? '')), finalize(() => this.inProgress = false)).subscribe((jwt) => {
      localStorage.setItem('jwt', jwt.access_token);
      localStorage.setItem('refresh', jwt.refresh_token);
      this.loginService.updateStatus(true);
      this.snackBarService.openSnackbar('Login Successful', 'success');
    });
  }

  facebookLogin(): Observable<string | undefined> {
      return from(new Promise<fb.StatusResponse>(resolve => FB.login(resolve, {scope: 'email'}))).pipe(concatMap(({ authResponse }) => {
        if (!authResponse){
          this.snackBarService.openSnackbar('Login rejected', 'error');
            return EMPTY;
        };
        return of(authResponse.accessToken);
      }));
  }

  logout() {
    this.loginService.logout();
}
}
