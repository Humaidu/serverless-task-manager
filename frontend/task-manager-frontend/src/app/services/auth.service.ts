import { Injectable } from '@angular/core';
import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails,
} from 'amazon-cognito-identity-js';

import { jwtDecode } from 'jwt-decode'; 
import { environment } from 'src/environments/environment';

// Configuration for AWS Cognito User Pool
const poolData = {
  UserPoolId: environment.cognito.userPoolId,
  ClientId: environment.cognito.clientId
};

// Create a CognitoUserPool instance from the above config
const userPool = new CognitoUserPool(poolData);

// Interface to type-check the decoded JWT token
interface DecodedToken {
  email: string;
  [key: string]: any; // Other optional fields like 'cognito:groups'
}

@Injectable({
  providedIn: 'root', // Makes this service available throughout the app
})
export class AuthService {
  userRole: string | null = null;

  /**
   * Logs in the user by authenticating credentials against Cognito.
   * If successful, stores the JWT token in localStorage.
   * @param email - The user's email (username)
   * @param password - The user's password
   * @returns A promise that resolves with the JWT token or rejects with an error
   */

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
          const idToken = result.getIdToken().getJwtToken(); // Extract the ID token
          localStorage.setItem('authToken', idToken); // Store in localStorage
          resolve(idToken);
        },
        onFailure: (err) => {
          reject(err); // Handle login failure
        },
      });
    });
  }

  /**
   * Retrieves the JWT token from localStorage.
   * @returns The token string or null if not found
   */
  getToken(): string | null {
    return localStorage.getItem('authToken');
  }

  /**
   * Decodes the JWT token into a usable object.
   * @returns A DecodedToken object or null if invalid or not found
   */
  getDecodedToken(): DecodedToken | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      return jwtDecode(token); // Decode without verifying signature (client-side only)
    } catch (err) {
      console.error('Invalid token', err);
      return null;
    }
  }

  /**
   * Extracts the email from the decoded JWT token.
   * @returns The user's email or null
   */
  getUserEmail(): string | null {
    const decoded = this.getDecodedToken();
    return decoded?.email || null;
  }

  /**
   * Extracts the user role from the 'cognito:groups' claim in the token.
   * @returns 'admin' if user belongs to Admin group, otherwise 'user'
   */
  getUserRole(): 'admin' | 'user' {
    const decoded = this.getDecodedToken();
    if (decoded?.['cognito:groups']?.includes('Admin')) return 'admin';
    return 'user';
  }

  /**
   * Checks if the user has the 'admin' role.
   * @returns true if admin, otherwise false
   */
  isAdmin(): boolean {
    return this.getUserRole() === 'admin';
  }

  /**
   * Checks if the user has the 'user' role.
   * @returns true if user, otherwise false
   */
  isUser(): boolean {
    return this.getUserRole() === 'user';
  }

  /**
   * Logs the user out by clearing the token and redirecting to login.
   */
  logout() {
    localStorage.removeItem('authToken'); // Clear token
    window.location.href = '/login'; // Redirect to login page
  }

  /**
   * Checks whether the user is currently logged in.
   * @returns true if token exists, otherwise false
   */
  isLoggedIn(): boolean {
    return !!localStorage.getItem('authToken');
  }
}
