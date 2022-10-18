================
Smart Widget :
================

Un SmartWidget est une classe Python qui génère un objet graphique à la demande. Il est prévu pour être affiché
sur une page HTML, particulièrement dans un environnement Django.

Il possède les caractéristiques suivantes :

- Il gère ses 'media' (au sens de Django, c'est à dire les fichiers de style CSS et les scripts JS).
- Il peut être hiérarchique (un widget peut être composé d'autres widgets)
- Il peut être créé soit de façon classique / statique, dans le code, par héritage d'autres classes Widget ou
  par création dynamique "au vol".
- Il a un mode de fonctionnement très déclaratif : Un widget est paramétrique et son code est exécuté à chaque rendu
  d'une vue Django pour créer une représentation graphique.
- Il peut être 'actif' au sens http car il a une porte d'entrée et peut donc recevoir des requêtes et les
  traiter [partie non implémentée, à finaliser...]

L'utilisation d'un widget se fait en X étapes :

- La classe est créée soit via le code python, soit par le biais de la `factory` qui est une méthode classe
  pour chaque Widget. La `factory` permet de créer dynamiquement, **au lancement de Django seulement**,
  (par exemple à partir d'un fichier de configuration) des classes de Widget.
- L'objet python widget est créé à partir de sa classe. **Méthode `__init__()`**
- La structure du widget est finalisée (ou créée si elle est dynamique). **Méthode setup()**.
- Les différents paramètres internes sont calculés, dans le widget et dans ses enfants (propagation) :
  **Méthode `parameters_process()`**. Le widget principal (*top level*) ne devrait prendre comme paramètres entrants
  que les paramètres de vue standards (utilisateur, requête, GET, POST, rôles de l'utilisateur,
  préférences de l'utilisateur, heure courante, etc.)
- Le contexte de rendu est créé à partir des paramètres transmis et/ou calculés et d'un *mapping* des variables.
  **Méthode `_get_context_data()`**. Il n'est normalement pas nécessaire de surcharger cette méthode.
- Enfin, le rendu final utilise le template et la liste des différents enfants, dont les différents contextes ont
  été calculés lors de l'étape précédente, pour générer le code HTML final. **Méthode `as_html()`**. Il n'est normalement pas nécessaire de surcharger cette méthode.

Idéalement, un widget doit être complètement déclaratif : La seule méthode qui devrait être surchargée est
`params_process()`. A terme, cette méthode pourra être totalement être défini avec une fonction déclarée
(à l'aide d'un objet SmartExpression venant, par exemple, d'un fichier de configuration ou d'une chaîne de
caractères).
