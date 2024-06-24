// Define the type of the environment variables.
declare interface Env {
  readonly NODE_ENV: string;
  // Replace the following with your own environment variables.
  // Example: NGX_VERSION: string;
  readonly FB_CLIENT_ID: string;
  readonly FB_REDIRECT: string;
  [key: string]: any;
}

declare interface ImportMeta {
  readonly env: Env;
}