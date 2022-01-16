export interface AuthenticationState {
  isLoggedIn?: boolean;
}

export const initialAuthenticationState: AuthenticationState = {
  isLoggedIn: undefined,
};
