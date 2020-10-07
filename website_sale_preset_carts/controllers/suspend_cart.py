# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRL fs
#   Rémy Taymans <remy@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import date, datetime, timedelta

from odoo import http
from odoo.http import request
from odoo.tools.translate import _


class WebsiteSuspendCart(http.Controller):
    @http.route("/cart/suspend", type="http", auth="user", website=True)
    def cart_suspend(self, **post):
        """Route to edit cart suspension dates."""
        form_context = {"partner": request.env.user.partner_id}
        data = request.params.copy()
        errors = {}
        if request.httprequest.method == "POST":
            cleaned_data, errors = self.clean_and_validate_form(data=data)
            if not errors:
                self.process_suspend_cart_form(
                    cleaned_data=cleaned_data, context=form_context
                )
                return request.redirect(
                    request.params.get("redirect")
                )
        qcontext = {
            "data": data,
            "initial": self.suspend_cart_form_initial(context=form_context),
            "errors": errors,
            "redirect": request.params.get("redirect") or "/my/home",
            "today": date.today().isoformat(),
        }
        return request.render(
            "website_sale_preset_carts.suspend_cart_form", qcontext
        )

    def suspend_cart_form_initial(self, context=None):
        """Return initial for suspend cart form."""
        context = {} if context is None else context
        initial = {}
        partner = context.get("partner")
        if partner.suspend_cart:
            initial["date_from"] = partner.cart_suspended_from
            initial["date_to"] = partner.cart_suspended_date
        else:
            initial["date_from"] = date.today().isoformat()
            initial["date_to"] = (date.today() + timedelta(days=1)).isoformat()
        return initial

    def clean_and_validate_form(self, data):
        """Return the cleaned data and errors."""
        cleaned_data = {}
        errors = {}
        # Date from
        field = "date_from"
        value = data.get(field)
        try:
            value = self.clean_and_validate_date_from(value, data=data)
            cleaned_data[field] = value
        except ValueError as err:
            errors.update({field: err})
        # Date to
        field = "date_to"
        value = data.get(field)
        try:
            value = self.clean_and_validate_date_from(value, data=data)
            cleaned_data[field] = value
        except ValueError as err:
            errors += {field: err}
        return cleaned_data, errors

    def clean_and_validate_date_from(self, value, data=None):
        """
        Return the cleaned value and Raise ValueError if the
        date_from is not valid.
        """
        if not value:
            raise ValueError(_("This field is required."))
        try:
            value_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(_("Wrong format for the date."))
        if value_date <= date.today():
            raise ValueError(_("Date can not be in the past."))
        return value

    def clean_and_validate_date_to(self, value, data=None):
        """
        Return the cleaned value and Raise ValueError if the
        date_to is not valid.
        """
        if not value:
            raise ValueError(_("This field is required."))
        try:
            value_date = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(_("Wrong format for the date."))
        try:
            date_from = datetime.strptime(
                data.get("date_from"), "%Y-%m-%d"
            ).date()
        except ValueError:
            date_from = date.today()
        if value_date <= date.today():
            raise ValueError(_("Date can not be in the past."))
        if value_date <= date_from:
            raise ValueError(_("End date can not be before begin date."))
        return value

    def process_suspend_cart_form(self, cleaned_data, context=None):
        """Process subscription share form."""
        partner = context.get("partner")
        vals = self.res_partner_vals(
            cleaned_data=cleaned_data, context=context
        )
        partner.write(vals)

    def res_partner_vals(self, cleaned_data, context=None):
        """Reutrn vals to update suspend cart value."""
        vals = {
            "suspend_cart": True,
            "cart_suspended_from": cleaned_data["date_from"],
            "cart_suspended_date": cleaned_data["date_to"],
        }
        return vals
