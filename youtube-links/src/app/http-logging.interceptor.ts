import { Injectable } from '@angular/core';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class HttpLoggingInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    console.log('Outgoing Request:', req);

    return next.handle(req).pipe(
      tap(
        event => {
          console.log('Response:', event);
        },
        error => {
          console.error('Error Response:', error);
        }
      )
    );
  }
}
