package main

import (
	"net/http"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"

	"github.com/MooncellWiki/prts-frontend-api/controller/widget"
)

func main() {
	// Echo instance
	e := echo.New()

	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins: []string{"http://prts.wiki", "https://prts.wiki", "http://api.prts.wiki", "https://api.prts.wiki", "http://localhost"},
		AllowHeaders: []string{echo.HeaderOrigin, echo.HeaderContentType, echo.HeaderAccept},
		AllowMethods: []string{
			http.MethodGet,
			http.MethodHead,
			http.MethodPut,
			http.MethodPatch,
			http.MethodPost,
			http.MethodDelete,
			http.MethodOptions,
		},
		AllowCredentials: true,
		ExposeHeaders: []string{
			"Last-Modified",
		},
		MaxAge: int((time.Minute * 15).Seconds()),
	}))

	e.Logger.Debug("`echo` has been initialized")

	// Routes
	e.Logger.Debug("initializing controllers...")

	e.GET("/widget/itemDemand/:itemName", widget.ItemDemand)

	e.Logger.Debug("controllers registered. starting http server...")
	// Start server
	e.Logger.Fatal(e.Start("0.0.0.0:3001"))
}
