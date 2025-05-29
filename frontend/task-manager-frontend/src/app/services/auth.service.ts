import { Injectable } from '@angular/core';
import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
} from 'amazon-cognito-identity-js';

import { jwtDecode } from 'jwt-decode'; // ✅ Correct

const poolData = {
  UserPoolId: 'eu-west-1_wWros4Xiv',
  ClientId: '38481kq3epcirm2vqfqafkk94u',
};

const userPool = new CognitoUserPool(poolData);

interface DecodedToken {
  email: string;
  [key: string]: any;
}

@Injectable({
  providedIn: 'root', // ✅ This makes AuthService globally available
})
export class AuthService {
  login(email: string, password: string): Promise<string> {
    const authDetails = new AuthenticationDetails({
      Username: email,
      Password: password,
    });

    const userData = {
      Username: email,
      Pool: userPool,
    };

    const cognitoUser = new CognitoUser(userData);

    return new Promise((resolve, reject) => {
      cognitoUser.authenticateUser(authDetails, {
        onSuccess: (result) => {
          const idToken = result.getIdToken().getJwtToken();
          localStorage.setItem('authToken', idToken);
          resolve(idToken);
        },
        onFailure: (err) => {
          reject(err);
        },
      });
    });
  }

  getToken(): string | null {
    return localStorage.getItem('authToken');
  }


  getDecodedToken(): DecodedToken | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      return jwtDecode(token);
    } catch (err) {
      console.error('Invalid token', err);
      return null;
    }
  }

  getUserEmail(): string | null {
    const decoded = this.getDecodedToken();
    return decoded?.email || null;
  }
}
