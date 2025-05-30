import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  role: string = '' ;
  email: string = '';

  constructor(public authService: AuthService) {}

  ngOnInit(): void {
    const decoded = this.authService.getDecodedToken();
    if (decoded) {
      this.email = decoded.email;
      this.role = this.authService.getUserRole();
    }
  }
  
  logout() {
    this.authService.logout();
  }

}
