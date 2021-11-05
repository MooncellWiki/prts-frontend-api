package widget

import (
	"net/http"

	"github.com/labstack/echo/v4"
)

func ItemDemand(c echo.Context) error {
	return c.String(http.StatusOK, c.Param("itemName"))
}
