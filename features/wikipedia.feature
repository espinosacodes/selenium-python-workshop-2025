Feature: Verificar título de artículo en Wikipedia

  Scenario: Buscar y verificar título de artículo de Python
    Given I am on the Wikipedia home page
    When I search for "Python (lenguaje de programación)"
    Then I should see the article title "Python" 