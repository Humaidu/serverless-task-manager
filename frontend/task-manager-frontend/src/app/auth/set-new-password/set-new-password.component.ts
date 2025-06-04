import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-set-new-password',
  templateUrl: './set-new-password.component.html',
  styleUrls: ['./set-new-password.component.css']
})
export class SetNewPasswordComponent {
  username!: string;
  tempPassword!: string;
  newPassword = '';
  error: string | null = null;

  constructor(
    private authService: AuthService, 
    private route: ActivatedRoute, 
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.username = params['username'];
      this.tempPassword = params['tempPassword'];
    });
  }
  

  onSubmit() {
    const role = this.authService.getUserRole();
    this.authService.completeNewPasswordChallenge(this.newPassword)
      .then(() => {
         // redirect to dashboard/home
         if (role === 'admin') {
          this.router.navigate(['/admin/all-tasks']);
         } else {
          this.router.navigate(['/user/user-tasks']);
         }
      })
      .catch((err: { message: string; }) => {
        this.error = err.message || 'Failed to set new password';
      });
  }
}
