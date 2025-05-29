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
    private auth: AuthService, 
    private router: Router,
    private toastr: ToastrService
  ) {}

  async login() {
    try {
      await this.auth.login(this.email, this.password);
      this.router.navigate(['/my-tasks']);

    } catch (err) {
      this.error = 'Login failed. Please check your credentials.';
      this.toastr.error(this.error)
    }
  }
}

