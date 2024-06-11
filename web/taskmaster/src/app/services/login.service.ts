import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { environment } from '../../environments/environment';
import { JWT } from '../models/jwt.model';
import { LoginData } from '../models/logindata.model';

@Injectable({
  providedIn: 'root',
})
export class LoginService {
  loginStatus$ = new Subject<boolean>();

  constructor(private http: HttpClient) {}

  login(loginData: LoginData): Observable<JWT> {
    let headers = new HttpHeaders();
    headers = headers.append('Content-Type', 'application/x-www-form-urlencoded');

    const body = new URLSearchParams();
    body.set('username', loginData.username);
    body.set('password', loginData.password);

    return this.http.post<JWT>(environment.apiUrl + '/token', body.toString(), {
      headers
    });
  }

  updateStatus(status: boolean) {
    this.loginStatus$.next(status);
  }
}