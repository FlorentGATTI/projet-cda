<template>
    <h2>Contact</h2>
</template>
    <v-container fluid class="about-container">
      <!-- En-tête de la page -->
      <v-row class="text-center">
        <v-col>
          <h1 class="main-title">À Propos de Nous</h1>
          <p class="subtitle">
            Découvrez l'équipe derrière ce projet et contactez-nous pour toute question.
          </p>
        </v-col>
      </v-row>
  
      <!-- Section de présentation de l'équipe -->
      <v-row class="team-section">
        <v-col cols="12" md="10" class="mx-auto">
          <h2>Notre Équipe</h2>
          <v-row>
            <v-col cols="12" md="4" v-for="member in teamMembers" :key="member.name">
              <v-card class="team-card">
                <v-img :src="member.image" class="team-image" contain></v-img>
                <v-card-title>{{ member.name }}</v-card-title>
                <v-card-subtitle>{{ member.role }}</v-card-subtitle>
                <v-card-text>{{ member.description }}</v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
  
      <!-- Section de formulaire de contact -->
      <v-row class="contact-section">
        <v-col cols="12" md="8" class="mx-auto">
          <h2>Contactez-Nous</h2>
          <v-form @submit.prevent="submitForm">
            <v-text-field
              label="Nom"
              v-model="contactForm.name"
              outlined
              required
            ></v-text-field>
  
            <v-text-field
              label="Email"
              v-model="contactForm.email"
              outlined
              required
            ></v-text-field>
  
            <v-textarea
              label="Message"
              v-model="contactForm.message"
              outlined
              required
            ></v-textarea>
  
            <v-btn color="primary" type="submit">Envoyer</v-btn>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'ContactPage',
    data() {
      return {
        teamMembers: [
          {
            name: 'Georgy SIMAK',
            role: 'Développeur Backend',
            description: 'Expert en API et en gestion de bases de données.',
            image: 'path_to_image_1.jpg'
          },
          {
            name: 'Vincent Leborgne',
            role: 'Développeur Frontend',
            description: 'Spécialiste en interfaces utilisateur réactives.',
            image: 'path_to_image_2.jpg'
          },
          {
            name: 'Florent GATTI',
            role: 'Chef de Projet',
            description: 'Responsable de la coordination de l\'équipe et du respect des délais.',
            image: 'path_to_image_3.jpg'
          },
        ],
        contactForm: {
          name: '',
          email: '',
          message: ''
        },
      };
    },
    methods: {
      submitForm() {
        // Logic for submitting the contact form
        console.log('Form Submitted:', this.contactForm);
      }
    }
  };
  </script>
  
  <style scoped>
  .about-container {
    margin-top: 40px;
    padding: 20px;
    background-color: #f5f5f5;
  }
  
  .main-title {
    color: #1976D2;
    font-size: 2.5em;
  }
  
  .subtitle {
    font-size: 1.2em;
    color: #666;
    margin-bottom: 40px;
  }
  
  .team-section {
    margin-bottom: 40px;
  }
  
  .team-card {
    text-align: center;
  }
  
  .team-image {
    height: 200px;
    width: 200px;
    margin: 0 auto 15px;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .contact-section {
    margin-top: 40px;
  }
  </style>