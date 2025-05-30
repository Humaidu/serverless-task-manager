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
    try {
      await this.authService.login(this.email, this.password);
      
      const role = this.authService.getUserRole();

      if (role === 'admin') {
        this.router.navigate(['/admin/all-tasks']);
      } else {
        this.router.navigate(['/user/user-tasks']);
      }

    } catch (err) {
      this.error = 'Login failed. Please check your credentials.';
      this.toastr.error(this.error)
    }
  }
}

