<template>
        <v-card class="login-card">
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
            <v-btn @click="submit" :disabled="!isFormValid || isLoading">
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
.v-card-title {
  color: white;
  text-align: center;
  margin-bottom: 10px;
}
.content-container {
  padding: 0;
}
.v-card-actions{
  display: flex;
  flex-direction: column;
}

.v-form {
  color: white !important;
}

.v-field--active input {
  color: red;
}

.v-btn{
  color: transparent !important;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.35);
  width: 250px;
}
.v-btn:hover{
  color: white !important;
}

.login-card {
  box-shadow: none !important;
  background-color: transparent !important;

}

.v-text-field >>> .v-input__slot {
  background-color: transparent !important;
  box-shadow: none !important;
  border: 1px solid #ccc !important;
}

.v-text-field >>> .v-input__slot:before,
.v-text-field >>> .v-input__slot:after {
  border: none !important;
}

.login-btn {
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
