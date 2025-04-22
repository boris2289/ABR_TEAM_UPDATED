import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  imports: [FormsModule, ReactiveFormsModule]
})
export class RegisterComponent {
  form: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.form = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  submitForm() {
    if (this.form.invalid) return;

    const { username, password } = this.form.value;

    this.authService.register(username, password).subscribe({
      next: (res) => {
        console.log('Registered successfully:', res);
        this.router.navigate(['/login']);
      },
      error: (err) => {
        console.error('Registration failed:', err);
      }
    });
  }
}
