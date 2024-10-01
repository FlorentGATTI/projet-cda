<template>
  <v-container class="login-container">
    <v-row align="center" justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h5">{{ isLogin ? 'Connexion' : 'Inscription' }}</v-card-title>
          <v-card-text>
            <v-form v-model="valid" ref="form">
              <v-text-field
                v-model="username"
                label="Nom d'utilisateur"
                :rules="[rules.required]"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Mot de passe"
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                :rules="[rules.required]"
                required
              ></v-text-field>
              <v-text-field
                v-if="!isLogin"
                v-model="confirmPassword"
                label="Confirmer le mot de passe"
                :type="showPassword ? 'text' : 'password'"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                :rules="[rules.required, rules.matchPassword]"
                required
              ></v-text-field>

              <!-- Section d'affichage des messages d'erreur -->
              <v-alert v-if="errorMessage" type="error" dismissible>{{ errorMessage }}</v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="submit" :disabled="!valid">
              {{ isLogin ? 'Connexion' : 'Inscription' }}
            </v-btn>
          </v-card-actions>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="toggleForm">
              {{ isLogin ? 'Créer un compte' : 'Déjà un compte ? Se connecter' }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'AuthPage',
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      valid: false,
      isLogin: true,
      errorMessage: '',
      rules: {
        required: value => !!value || 'Champ requis.',
        matchPassword: value =>
          value === this.password || 'Les mots de passe ne correspondent pas.',
      },
    };
  },
  methods: {
    toggleForm() {
      this.isLogin = !this.isLogin;
      this.resetForm();
    },
    resetForm() {
      this.username = '';
      this.password = '';
      this.confirmPassword = '';
      this.errorMessage = '';
      this.$refs.form.reset();
    },
    async submit() {
      if (!this.isLogin && this.password !== this.confirmPassword) {
        this.errorMessage = 'Les mots de passe ne correspondent pas.';
        return;
      }

      if (this.$refs.form.validate()) {
        const endpoint = this.isLogin ? '/api/login' : '/api/register';
        try {
          const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: this.username,
              password: this.password,
            }),
          });

          if (!response.ok) {
            // Gestion des erreurs basées sur le code de statut HTTP
            if (response.status === 401) {
              this.errorMessage = 'Identifiants incorrects. Veuillez réessayer.';
            } else if (response.status === 400) {
              this.errorMessage = 'Requête invalide. Veuillez vérifier les informations saisies.';
            } else {
              this.errorMessage = 'Une erreur est survenue. Veuillez réessayer plus tard.';
            }
            throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();
          // Sauvegarde de l'utilisateur dans localStorage
          localStorage.setItem('user', JSON.stringify(data));
          // Redirection après le login ou l'inscription
          this.$router.push('/');
        } catch (error) {
          console.error('Error:', error.message);
        }
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
