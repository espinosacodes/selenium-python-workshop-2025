Feature: Verificar búsqueda de productos en MercadoLibre

  Scenario: Buscar iPhone 13 y verificar resultados
    Given I am on the MercadoLibre home page
    When I search for product "iPhone 13" in MercadoLibre
    Then I should see MercadoLibre search results containing "iPhone" 