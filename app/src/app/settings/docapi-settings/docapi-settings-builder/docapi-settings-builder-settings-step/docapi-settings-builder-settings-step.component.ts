/*
* DATAGERRY - OpenSource Enterprise CMDB
* Copyright (C) 2019 NETHINKS GmbH
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as
* published by the Free Software Foundation, either version 3 of the
* License, or (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU Affero General Public License for more details.

* You should have received a copy of the GNU Affero General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

import { Component, OnInit, Input } from '@angular/core';
import { CmdbMode } from '../../../../framework/modes.enum';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'cmdb-docapi-settings-builder-settings-step',
  templateUrl: './docapi-settings-builder-settings-step.component.html',
  styleUrls: ['./docapi-settings-builder-settings-step.component.scss']
})
export class DocapiSettingsBuilderSettingsStepComponent implements OnInit {

  @Input() public mode: CmdbMode;
  public modes = CmdbMode;
  public settingsForm: FormGroup;

  constructor() { 
    this.settingsForm = new FormGroup({
      name: new FormControl('', Validators.required),
      label: new FormControl('', Validators.required),
      description: new FormControl(''),
      active: new FormControl(true)
    });
  }

  public get name() {
    return this.settingsForm.get('name');
  }

  public get label() {
    return this.settingsForm.get('label');
  }


  ngOnInit() {
  }

}
