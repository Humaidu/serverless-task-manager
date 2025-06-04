import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';
import { Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  password = '';
  error = '';

  constructor(
    private authService: AuthService, 
    private router: Router,
    private toastr: ToastrService
  ) {}

  async login() {
    const role = this.authService.getUserRole();
    this.authService.login(this.email, this.password).then(async result => {
      if (result === 'NEW_PASSWORD_REQUIRED') {
        // Navigate to set-new-password page
        this.router.navigate(['/set-new-password'], {
          queryParams: {
            username: this.email,
            tempPassword: this.password
          }
        });
      } else {
        // Redirect to home/dashboard
        if (role === 'admin') {
          this.router.navigate(['/admin/all-tasks']);
        } else {
          this.router.navigate(['/user/user-tasks']);
        }
      }
    }).catch(err => {
      console.error('Login failed', err);
      this.error = 'Login failed. Please check your credentials.';
      this.toastr.error(this.error)
    });
  }
}

