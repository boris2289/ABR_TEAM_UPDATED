import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:1278/api/login/';
  private tokenKey = 'authToken';

  constructor(private http: HttpClient, @Inject(PLATFORM_ID) private platformId: Object) {}

  login(username: string, password: string): Observable<any> {
    const body = { username, password };
    console.log(this.http.post<any>(this.apiUrl, body));
    return this.http.post<any>(this.apiUrl, body);
  }

  saveToken(token: string): void {
    console.log('Saving token:', token); 
    localStorage.setItem(this.tokenKey, token);

  }

  getToken(): string | null {
    const token = localStorage.getItem(this.tokenKey);
    console.log('Fetched token:', token); 
    return token;
    return null;
  }

  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
  
  register(username: string, password: string): Observable<any> {
    const body = { username, password };
    const url = 'http://127.0.0.1:1278/register/';
    return this.http.post<any>(url, body);
  }
}
