import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { MatButtonModule } from '@angular/material/button'
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import {MatCardModule} from '@angular/material/card';
import { ReactiveFormsModule } from '@angular/forms';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-login',
  templateUrl: './login.component.html',
  imports: [ReactiveFormsModule, MatCardModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  styleUrls: ['./login.component.css'],
})

export class LoginComponent {
  form = new FormGroup({
    username: new FormControl<string>('', Validators.required),
    password: new FormControl<string>('', Validators.required),
  });

  constructor(private authService: AuthService, private router: Router) {}

  submitForm() {
    if (this.form.invalid) return;

    const username = this.form.get('username')?.value ?? '';
    const password = this.form.get('password')?.value ?? '';

    this.authService.login(username, password).subscribe(
      (response) => {
        alert(JSON.stringify(response)); 
        const token = response.token;  
        this.authService.saveToken(token);
        this.router.navigate(['/youtube-links']);
      },
      (error) => {
        console.error('Login error:', error);
      }
    );
  }
}