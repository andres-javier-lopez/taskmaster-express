import { LoginService } from "../app/services/login.service";
import { environment } from "../environments/environment";

export function appInitializer(loginService: LoginService) {
  
  return () => new Promise<void>(resolve => {
    // load facebook sdk script
    (function(d, s, id){
        let js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s) as HTMLElement & { src: string };
        js.id = id;
        js.src = "https://connect.facebook.net/en_US/sdk.js";
        fjs.parentNode?.insertBefore(js, fjs);
      }(document, 'script', 'facebook-jssdk')
    );

    // wait for facebook sdk to initialize before starting the angular app
    window['fbAsyncInit'] = function () {
      FB.init({
        appId: environment.facebookAppId,
        cookie: true,
        xfbml: true,
        version: 'v8.0'
      });

      FB.AppEvents.logPageView();
      
      FB.getLoginStatus(({authResponse}) => {
        if (authResponse?.accessToken) {
            loginService.apiAuthenticate(authResponse.accessToken)
                .subscribe((jwt) => {
                  localStorage.setItem('jwt', jwt.access_token);
                  localStorage.setItem('refresh', jwt.refresh_token);
                  loginService.updateStatus(true);
                })
                .add(resolve);
        } else {
            resolve();
        }
      });
    };
  });
}