export class JWT {
  constructor(
    public access_token: string,
    public refresh_token: string,
    public token_type: string,
  ) {}
}
