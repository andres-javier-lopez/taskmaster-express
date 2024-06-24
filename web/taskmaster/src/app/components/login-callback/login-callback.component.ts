import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subject } from 'rxjs';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-login-callback',
  standalone: true,
  imports: [],
  templateUrl: './login-callback.component.html',
  styleUrl: './login-callback.component.scss'
})
export class LoginCallbackComponent implements OnInit, OnDestroy{
  unsubscribe$ = new Subject<void>();

  constructor(private activatedRoute: ActivatedRoute, private route: Router, private loginService: LoginService) {}

  ngOnInit(): void {
    this.activatedRoute.fragment.subscribe((fragment: string | null) => {
      if (fragment?.includes("access_token")) {
        const accessToken = fragment.split('=')[1];
        this.loginService.apiAuthenticate(accessToken).subscribe((jwt) => {
          localStorage.setItem('jwt', jwt.access_token);
          localStorage.setItem('refresh', jwt.refresh_token);
          this.loginService.updateStatus(true);
          this.route.navigate(['']);  
        });
      } else {
        this.route.navigate(['']);
      }
    });
  }

  ngOnDestroy(): void {
    this.unsubscribe$.next();
    this.unsubscribe$.complete();
  }

}
