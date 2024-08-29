<template>
    <v-container class="login-container">
      <v-row align="center" justify="center">
        <v-col cols="12" md="6">
          <v-card>
            <v-card-title class="text-h5">{{ isLogin ? 'Login' : 'Register' }}</v-card-title>
            <v-card-text>
              <v-form v-model="valid" ref="form">
                <v-text-field
                  v-model="username"
                  label="Username"
                  :rules="[rules.required]"
                  required
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  label="Password"
                  :type="showPassword ? 'text' : 'password'"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append="showPassword = !showPassword"
                  :rules="[rules.required]"
                  required
                ></v-text-field>
                <v-text-field
                  v-if="!isLogin"
                  v-model="confirmPassword"
                  label="Confirm Password"
                  :type="showPassword ? 'text' : 'password'"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append="showPassword = !showPassword"
                  :rules="[rules.required, matchPassword]"
                  required
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="submit" :disabled="!valid">
                {{ isLogin ? 'Login' : 'Register' }}
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
        rules: {
          required: value => !!value || 'Required.',
          matchPassword: value => value === this.password || 'Passwords must match.',
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
        this.$refs.form.reset();
      },
      submit() {
        if (this.$refs.form.validate()) {
          if (this.isLogin) {
            // Handle login logic here
            console.log('Logging in with', this.username, this.password);
          } else {
            // Handle registration logic here
            console.log('Registering with', this.username, this.password, this.confirmPassword);
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
  