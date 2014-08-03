function Astral(auth_token, username) {
  this.auth_token = auth_token;
  this.username = username;
}

Astral.prototype.payWithAstral = function(price) {
  // redirect to my site with params
  window.location.href = "http://localhost:5000/pay?username="+ encodeURIComponent(this.username) + "&auth_token="+ encodeURIComponent(this.auth_token) + "&price="+ encodeURIComponent(price);
};

Astral.prototype.buyAstralGiftCard = function(price) {
  // redirect to my site with params
  window.location.href = "http://localhost:5000/gift?username="+ encodeURIComponent(this.username) + "&auth_token="+ encodeURIComponent(this.auth_token)+ "&price="+ encodeURIComponent(price);
};
