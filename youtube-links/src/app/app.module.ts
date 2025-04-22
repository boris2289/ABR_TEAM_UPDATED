import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { YoutubeLinksComponent } from './youtube-links/youtube-links.component';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common'; 
import { FormsModule } from '@angular/forms';
import { NgForm } from '@angular/forms';
import { NgModel } from '@angular/forms';
import { LoginComponent } from './login/login.component';
import { HttpLoggingInterceptor } from './http-logging.interceptor';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { RegisterComponent } from './register/register.component';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    YoutubeLinksComponent,
    LoginComponent,
    HttpClientModule,
    CommonModule,
    FormsModule,
    RegisterComponent
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: HttpLoggingInterceptor,
      multi: true 
    },     provideClientHydration(withEventReplay())
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
