## RESIDENCE_SHAMMA

## Data base, necessary tables/models:
- Department:
    - id
    - name

<!-- - RoomType( en fonction du nombre de pieces):
    - id
    - type_name -->

- RoomCategory(en fonction des prix):
    - name
    - price

- Customer:
    - relation with User models for authenticating users, User model contains:  
        - username
        - last_name
        - first_name
        - email
        - password
    - contact1
    - contact2            

- Invoice:
    - name(concatenation of customer name and number)    
    - total_amount
    - amount_paid
    - amount_due
    - paid (Boolean indicating whether the invoice is fully paid or not )

- Room:
    - name
    - available
    - description 
    - department(ForeignKey for Department)
    - category(ForeignKey for RoomCategory)
    <!-- - room_type(ForeignKey for RoomType) -->

- Reservation:
    - customer(ForeignKey for Customer)
    - invoice(ForeignKey for Invoice)
    - room(ForeignKey for Room)
    - check_in_date
    - check_out_date
    - created_at

- Review:
    - Reservation (ForeignKey for Reservation)
    - user (ForeignKey for User) 
    - comment
    - rating
    - created_at   


##  Website features:
- General:  
    - [] Présentation aléatoire des résidences.   
    - [] Menu avec: 
        - catégories déroulantes : permet aux utilisateurs de sélectionner une catégorie et de voir les appartements correspondants.
        - types déroulants
    - [] Creation de support lingustique: FR & EN    
- User:  
    - Authentification system:
        - Permettre de s'inscire normalement, avec l'API OAuth2 de google
        - Permettre de se connecter
        - Permettre de se deconnecter
    - [] Affichage des détails de la résidence : description, emplacement, images supplémentaires.
    - [] Invitation à créer un compte pour confirmer la réservation.
    - [] Saisie des informations de réservation après création du compte.    
    - [] Paiement d'un premier versement pour confirmer la réservation.
    - [] Association automatique de la facture, du client et de la chambre dans la table de réservation.
    - [] Permettre le commentaire et la notation des reservations

## Comportement du site:  

1. Création d'un compte utilisateur:  
    - L'utilisateur accède à la page d'inscription et fournit les informations nécessaires pour créer un compte utilisateur (nom d'utilisateur, adresse e-mail, mot de passe, etc.).
    - Le système vérifie les données et crée un nouveau compte utilisateur.

2. Connexion à un compte utilisateur :

    - L'utilisateur accède à la page de connexion et entre ses identifiants (nom d'utilisateur et mot de passe).
    - Le système vérifie les identifiants et authentifie l'utilisateur.

3. Recherche de chambres disponibles :

    - L'utilisateur accède à la page de recherche de chambres.
    - Il sélectionne les critères de recherche tels que la date d'arrivée, la date de départ, le nombre de personnes, etc.
    - Le système affiche les chambres disponibles correspondant aux critères de recherche.

4. Sélection d'une chambre et réservation :

    - L'utilisateur sélectionne une chambre disponible.
    - Il fournit les détails de réservation tels que la date d'arrivée, la date de départ, etc.
    - Le système vérifie la disponibilité de la chambre pour les dates spécifiées et crée une réservation si la chambre est disponible.
    - Une facture est automatiquement générée pour la réservation, calculant le montant total en fonction du prix de la chambre et de la durée de la réservation.
    - L'utilisateur peut procéder au paiement initial de la réservation.
    - ## PLUS DE DETAILS:
        4.1. Sélection de la chambre et fourniture des détails de la réservation :

            - L'utilisateur sélectionne une chambre disponible à partir de la liste des chambres disponibles affichées sur la page de recherche.
            - Il fournit les détails de la réservation tels que la date d'arrivée, la date de départ, le nombre de personnes, etc. à l'aide d'un formulaire de réservation.

        4.2. Vérification de la disponibilité et création de la réservation :

            - Une fois que l'utilisateur soumet le formulaire de réservation, le système vérifie la disponibilité de la chambre pour les dates spécifiées.
            - Si la chambre est disponible, le système crée une nouvelle réservation associée à la chambre sélectionnée et au client correspondant.

        4.3. Calcul du montant total et création de la facture :

            - Après la création de la réservation, le système calcule automatiquement le montant total de la réservation en fonction du prix de la chambre et de la durée du séjour.
            - Une nouvelle facture est automatiquement créée pour cette réservation avec le montant total calculé.

        4.4. Paiement initial de la réservation :

            - Une fois la réservation créée et la facture générée, l'utilisateur est redirigé vers la page de paiement.
            - Il effectue le paiement initial de la réservation en utilisant un formulaire de paiement en ligne sécurisé.
            - Après le paiement réussi, le montant payé est enregistré dans la facture comme montant déjà payé.

        4.5. Mise à jour de la disponibilité de la chambre :

            - Après le paiement réussi, la chambre réservée devient indisponible pour les dates spécifiées.
            - Le système met à jour le statut de disponibilité de la chambre dans la base de données pour refléter qu'elle est maintenant réservée pour ces dates.

5. Consultation des réservations et gestion du compte :
 
    - L'utilisateur peut accéder à la page de son compte où il peut voir ses réservations passées, les détails de la facture, etc.
    - Il peut également mettre à jour ses informations personnelles, ajouter des contacts supplémentaires, etc.

6. Ajout de commentaires et évaluation des séjours :

    - Après avoir séjourné dans une chambre, l'utilisateur peut accéder à la page de commentaires et évaluation.
    - Il peut laisser un commentaire sur son expérience et attribuer une note à la chambre.