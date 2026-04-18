const TRANSLATIONS = {
    en: {
        app_name: 'RspamdHotOrNot',
        nav_dashboard: 'Dashboard',
        nav_review: 'Review',
        nav_history: 'History',
        nav_settings: 'Settings',
        nav_logout: 'Logout',
        loading: 'Loading...',
        loading_prep: 'Preparing...',

        login_title: 'RspamdHotOrNot - Login',
        username: 'Username',
        password: 'Password',
        sign_in: 'Sign In',
        login_failed: 'Login failed',
        login_error_prefix: 'Login error: ',

        first_login_title: 'First Login - RspamdHotOrNot',
        security_first: 'Security first',
        first_login_subtitle: 'Please change your username and password at first login.',
        current_password: 'Current password',
        new_username: 'New username',
        new_password: 'New password',
        confirm_new_password: 'Confirm new password',
        save_securely: 'Save securely',
        passwords_mismatch: 'The new passwords do not match.',
        update_failed: 'Update failed',
        save_error_prefix: 'Save error: ',

        dashboard_title: 'Dashboard',
        pending_reviews: 'Pending reviews',
        spam_today: 'Spam today',
        ham_today: 'Ham today',
        total_processed: 'Total processed',
        new_mail_last_sync: 'New mails last sync',
        duplicates: 'Duplicates',
        no_sync_yet: 'No sync yet',
        last_sync_prefix: 'Last sync',
        sync_mails: 'Sync mails',
        go_to_review: 'Go to review',
        recent_activities: 'Recent activities',
        no_activities: 'No activities',
        sync_success_prefix: 'Synced',
        sync_success_new: 'new mails',
        sync_success_dupes: 'duplicates',
        sync_error_prefix: 'Sync error: ',

        review_title: 'Mail review',
        no_open_mails: 'No open mails for review',
        back_to_dashboard: 'Back to dashboard',
        from: 'From',
        to: 'To',
        date: 'Date',
        unknown: 'Unknown',
        no_subject: '(No subject)',
        no_body: '(No body)',
        shortened: '[...shortened...]',
        not_spam: 'Not spam',
        spam: 'Spam',
        skip: 'Skip',
        load_mail_error: 'Error loading mail',
        save_error: 'Error while saving',
        skip_error: 'Error while skipping',
        error_prefix: 'Error: ',

        history_title: 'Classification history',
        search_placeholder: 'Search...',
        col_datetime: 'Date/Time',
        col_sender: 'Sender',
        col_subject: 'Subject',
        col_decision: 'Decision',
        col_rspamd: 'Rspamd',
        no_history: 'No history',
        load_history_error: 'Error loading history',
        decision_ham: 'Not spam',
        decision_skipped: 'Skipped',

        settings_title: 'Settings',
        mail_source: 'Mail source',
        current_source: 'Current source',
        source_note: 'The mail source is configured via the .env file.',
        rspamd_integration: 'Rspamd integration',
        status: 'Status',
        connected: 'Connected',
        disabled: 'Disabled',
        rspamd_note: 'Rspamd connection is checked at startup.',
        info: 'Info',
        timezone: 'Timezone',
        timezone_note: 'Select preferred timezone for timestamps.',
        save: 'Save',
        timezone_saved_prefix: 'Timezone saved',
        language: 'Language',
        language_note: 'Select UI language.',
        language_saved_prefix: 'Language saved',
        change_credentials: 'Change credentials',
        credentials_note: 'Change username and password for the current account.',
        confirm_password: 'Confirm new password',
        save_credentials: 'Save credentials',
        fill_all_fields: 'Please fill in all fields.',
        min_password_length: 'New password must be at least 8 characters.',
        save_failed: 'Error while saving.',
        credentials_changed: 'Credentials changed successfully.',
        management: 'Management',
        reset_db: 'Reset database',
        reset_warning: 'This will delete all classifications.',
        confirm_reset: 'All data will be deleted. Continue?'
    },
    de: {
        app_name: 'RspamdHotOrNot',
        nav_dashboard: 'Dashboard',
        nav_review: 'Pruefen',
        nav_history: 'Verlauf',
        nav_settings: 'Einstellungen',
        nav_logout: 'Abmelden',
        loading: 'Wird geladen...',
        loading_prep: 'Wird vorbereitet...',

        login_title: 'RspamdHotOrNot - Login',
        username: 'Benutzername',
        password: 'Passwort',
        sign_in: 'Anmelden',
        login_failed: 'Login fehlgeschlagen',
        login_error_prefix: 'Fehler beim Login: ',

        first_login_title: 'Erst-Anmeldung - RspamdHotOrNot',
        security_first: 'Sicherheit zuerst',
        first_login_subtitle: 'Bitte aendere bei der ersten Anmeldung Benutzername und Passwort.',
        current_password: 'Aktuelles Passwort',
        new_username: 'Neuer Benutzername',
        new_password: 'Neues Passwort',
        confirm_new_password: 'Neues Passwort wiederholen',
        save_securely: 'Sicher speichern',
        passwords_mismatch: 'Die neuen Passwoerter stimmen nicht ueberein.',
        update_failed: 'Aktualisierung fehlgeschlagen',
        save_error_prefix: 'Fehler beim Speichern: ',

        dashboard_title: 'Dashboard',
        pending_reviews: 'Offene Pruefungen',
        spam_today: 'Spam heute',
        ham_today: 'Ham heute',
        total_processed: 'Gesamt bearbeitet',
        new_mail_last_sync: 'Neue Mails letzter Sync',
        duplicates: 'Duplikate',
        no_sync_yet: 'Noch kein Sync',
        last_sync_prefix: 'Letzter Sync',
        sync_mails: 'Mails synchronisieren',
        go_to_review: 'Zur Pruefseite',
        recent_activities: 'Letzte Aktivitaeten',
        no_activities: 'Keine Aktivitaeten',
        sync_success_prefix: 'Synchronisiert',
        sync_success_new: 'neue Mails',
        sync_success_dupes: 'Duplikate',
        sync_error_prefix: 'Fehler beim Synchronisieren: ',

        review_title: 'Mail-Pruefung',
        no_open_mails: 'Keine offenen Mails zur Pruefung',
        back_to_dashboard: 'Zum Dashboard',
        from: 'Von',
        to: 'An',
        date: 'Datum',
        unknown: 'Unbekannt',
        no_subject: '(Kein Betreff)',
        no_body: '(Kein Body)',
        shortened: '[...gekuerzt...]',
        not_spam: 'Kein Spam',
        spam: 'Spam',
        skip: 'Ueberspringen',
        load_mail_error: 'Fehler beim Laden der Mail',
        save_error: 'Fehler beim Speichern',
        skip_error: 'Fehler beim Ueberspringen',
        error_prefix: 'Fehler: ',

        history_title: 'Klassifizierungsverlauf',
        search_placeholder: 'Suchen...',
        col_datetime: 'Datum/Uhrzeit',
        col_sender: 'Absender',
        col_subject: 'Betreff',
        col_decision: 'Entscheidung',
        col_rspamd: 'Rspamd',
        no_history: 'Kein Verlauf',
        load_history_error: 'Fehler beim Laden',
        decision_ham: 'Kein Spam',
        decision_skipped: 'Uebersprungen',

        settings_title: 'Einstellungen',
        mail_source: 'Mail-Quelle',
        current_source: 'Aktuelle Quelle',
        source_note: 'Die Mail-Quelle wird aus der .env-Datei konfiguriert.',
        rspamd_integration: 'Rspamd-Integration',
        status: 'Status',
        connected: 'Verbunden',
        disabled: 'Deaktiviert',
        rspamd_note: 'Rspamd-Verbindung wird beim Start ueberprueft.',
        info: 'Info',
        timezone: 'Zeitzone',
        timezone_note: 'Gewuenschte Zeitzone fuer Zeitstempel auswaehlen.',
        save: 'Speichern',
        timezone_saved_prefix: 'Zeitzone gespeichert',
        language: 'Sprache',
        language_note: 'Anzeigesprache auswaehlen.',
        language_saved_prefix: 'Sprache gespeichert',
        change_credentials: 'Zugangsdaten aendern',
        credentials_note: 'Benutzernamen und Passwort fuer den aktuellen Account aendern.',
        confirm_password: 'Neues Passwort bestaetigen',
        save_credentials: 'Zugangsdaten speichern',
        fill_all_fields: 'Bitte alle Felder ausfuellen.',
        min_password_length: 'Neues Passwort muss mindestens 8 Zeichen haben.',
        save_failed: 'Fehler beim Speichern.',
        credentials_changed: 'Zugangsdaten erfolgreich geaendert.',
        management: 'Verwaltung',
        reset_db: 'Datenbank zuruecksetzen',
        reset_warning: 'Dies wird alle Klassifizierungen loeschen.',
        confirm_reset: 'Alle Daten werden geloescht. Fortfahren?'
    }
};

function getLanguage() {
    return localStorage.getItem('app_language') || 'en';
}

function setLanguage(language) {
    const normalized = language === 'de' ? 'de' : 'en';
    localStorage.setItem('app_language', normalized);
    document.documentElement.lang = normalized;
    return normalized;
}

function t(key) {
    const language = getLanguage();
    const langDict = TRANSLATIONS[language] || TRANSLATIONS.en;
    return langDict[key] || TRANSLATIONS.en[key] || key;
}

function getLocale() {
    return getLanguage() === 'de' ? 'de-DE' : 'en-US';
}

function getTimezone() {
    return localStorage.getItem('app_timezone') || Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
}

function formatDateLocalized(value) {
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString(getLocale(), { timeZone: getTimezone() });
}

function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach((element) => {
        const key = element.getAttribute('data-i18n');
        element.textContent = t(key);
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach((element) => {
        const key = element.getAttribute('data-i18n-placeholder');
        element.setAttribute('placeholder', t(key));
    });

    document.querySelectorAll('[data-i18n-title]').forEach((element) => {
        const key = element.getAttribute('data-i18n-title');
        element.setAttribute('title', t(key));
    });

    document.querySelectorAll('[data-i18n-html]').forEach((element) => {
        const key = element.getAttribute('data-i18n-html');
        element.innerHTML = t(key);
    });
}

(function initI18n() {
    setLanguage(getLanguage());
})();
