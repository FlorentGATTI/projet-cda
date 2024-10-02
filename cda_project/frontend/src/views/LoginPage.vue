<template>
  <v-container class="login-container">
    <v-row align="center" justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title class="text-h5">{{ isLogin ? "Connexion" : "Inscription" }}</v-card-title>
          <v-card-text>
            <v-form v-model="isFormValid" ref="form">
              <v-text-field v-model="username" label="Nom d'utilisateur" :rules="[rules.required]" required> </v-text-field>

              <v-text-field v-model="password" label="Mot de passe" :type="showPassword ? 'text' : 'password'" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" @click:append="showPassword = !showPassword" :rules="[rules.required, rules.minLength]" required> </v-text-field>

              <v-text-field v-if="!isLogin" v-model="confirmPassword" label="Confirmer le mot de passe" :type="showPassword ? 'text' : 'password'" :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'" @click:append="showPassword = !showPassword" :rules="[rules.required, rules.matchPassword]" required> </v-text-field>

              <!-- Section d'affichage des messages d'erreur -->
              <v-alert v-if="errorMessage" type="error" dismissible>{{ errorMessage }}</v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" @click="submit" :disabled="!isFormValid || isLoading">
              {{ isLogin ? "Connexion" : "Inscription" }}
            </v-btn>
          </v-card-actions>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="toggleForm">
              {{ isLogin ? "Créer un compte" : "Déjà un compte ? Se connecter" }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";

export default {
  name: "LoginPage",
  setup() {
    const router = useRouter();
    const form = ref(null);
    const username = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const showPassword = ref(false);
    const isLogin = ref(true);
    const errorMessage = ref("");
    const isFormValid = ref(false);
    const isLoading = ref(false);

    const rules = reactive({
      required: (v) => !!v || "Champ requis",
      minLength: (v) => v.length >= 4 || "Le mot de passe doit contenir au moins 4 caractères",
      matchPassword: (v) => v === password.value || "Les mots de passe ne correspondent pas",
    });

    const toggleForm = () => {
      isLogin.value = !isLogin.value;
      errorMessage.value = "";
      username.value = "";
      password.value = "";
      confirmPassword.value = "";
      if (form.value) form.value.resetValidation();
    };

    const submit = async () => {
      if (!isFormValid.value) return;

      isLoading.value = true;
      errorMessage.value = "";

      const endpoint = isLogin.value ? "/api/login" : "/api/register";
      try {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: username.value, password: password.value }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Une erreur est survenue");
        }

        localStorage.setItem("user", JSON.stringify(data));
        router.push("/");
      } catch (error) {
        console.error("Error:", error);
        errorMessage.value = error.message || "Erreur de connexion au serveur. Veuillez réessayer plus tard.";
      } finally {
        isLoading.value = false;
      }
    };

    return {
      form,
      username,
      password,
      confirmPassword,
      showPassword,
      isLogin,
      errorMessage,
      rules,
      isFormValid,
      isLoading,
      toggleForm,
      submit,
    };
  },
};
</script>

<style scoped>
.v-card-actions{
  display: flex;
  flex-direction: column;
}

.v-btn{
  color: white !important;
}

.login-card {
  box-shadow: none !important;
  background-color: transparent !important;
}

.login-title {
  background-color: transparent;
  color: #1976d2;
}

.v-text-field >>> .v-input__slot {
  background-color: white !important;
  box-shadow: none !important;
  border: 1px solid #ccc !important;
}

.v-text-field >>> .v-input__slot:before,
.v-text-field >>> .v-input__slot:after {
  border: none !important;
}

.login-btn {
  background-color: #1976d2 !important;
  color: white !important;
  font-weight: 500;
  height: 44px;
  text-transform: none;
  font-size: 16px;
}

.register-btn {
  color: #1976d2 !important;
  font-weight: 500;
  height: 44px;
  font-size: 16px;
}

.v-btn {
  text-transform: none;
  letter-spacing: normal;
}
</style>
