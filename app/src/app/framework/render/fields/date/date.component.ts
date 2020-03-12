import { Component, OnInit } from '@angular/core';
import { RenderField } from '../components.fields';
import { formatDate } from '@angular/common';
import { NgbDateAdapter, NgbDateNativeAdapter, NgbDateStruct} from '@ng-bootstrap/ng-bootstrap';
import { NgbStringAdapter } from './NgbStringAdapter';

@Component({
  selector: 'cmdb-date',
  templateUrl: './date.component.html',
  styleUrls: ['./date.component.scss'],
  providers: [{provide: NgbDateAdapter, useClass: NgbStringAdapter}]
})
export class DateComponent extends RenderField implements  OnInit {

  public constructor() {
    super();
  }

  ngOnInit(): void {
    if (this.data.default !== undefined) {
      const temp = this.data.default;
      this.data.default = temp.year + '-' + temp.month + '-' + temp.day;
    }
    if (this.parentFormGroup.get(this.data.name).value === '') {
      this.parentFormGroup.get(this.data.name).setValue(null, {onlySelf: true});
    }
  }

  public get currentDate() {
    const currentDate = this.parentFormGroup.get(this.data.name).value;
    if (currentDate && currentDate.$date) {
      return new Date(currentDate.$date);
    }
    return currentDate;
  }
}
