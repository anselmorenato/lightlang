#ifndef SETTINGSWIDGET_H
#define SETTINGSWIDGET_H

#include <QtGui/QDialog>

class QLabel;
class QDoubleSpinBox;
class QCheckBox;
class InfoButton;
class PopupWindow;

class SettingsWidget : public QDialog
{
	Q_OBJECT
	signals:
		void updateSettings();
	public slots:
		void saveSettings();
	public:
		SettingsWidget(QWidget *parent = 0);
		~SettingsWidget();
		
		int translationRenovation() const;
		bool useStatuses() const;
		bool useHighlighting() const;
		bool showTips() const;
		
		void loadSettings();
	private:
		QLabel *headerLabel;
		QLabel *introductionLabel;
	
		QDoubleSpinBox *updateTranslationTimeSpinBox;
		QCheckBox *useHighlightingCheckBox;
		QCheckBox *useStatusesCheckBox;
		QCheckBox *showTipsCheckBox;
	
		PopupWindow *popupWindow;
		InfoButton *updateTranslationInfoButton;
		InfoButton *useHighlightingInfoButton;
		InfoButton *useStatusesInfoButton;
		InfoButton *showTipsInfoButton;
};

#endif